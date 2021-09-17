# Project Card Registry Template 
A template repository for Network Wrangler Project Card registries.

[Network Wrangler 2.0](https://github.com/wsp-sag/network_wrangler) is a Python library for managing travel model network scenarios. Network Wrangler uses `Project Cards` to define network edits. The purpose of this repository is to automate the reconciliation of conflicting Project Cards.

Consider, for example, an existing base year network that includes nodes A, B, and C. Project Card X extends Main Street, adding Node 1 at Location Alpha. Project Card Y extends Broad Street, adding a different node at Location Beta, but also labeling the new node Node 1. In the current Network Wrangler framework, users must manually manage the conflicting `Node 1` definitions. The purpose of this repository is to automate the node (and link) numbering process via a registry.

## Instructions
1. This repository is a [`template`](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template), meaning it is designed to be used to create repositories that have the same functionality.
2. To get started, open up the `registry_config.yml` file in a text editor. This file defines the allowable range of the `model_node_id` and `model_link_id` fields using the `minimum_allowable_node_id`, `maximum_allowable_node_id`, `minimum_allowable_link_id` and `maxmimum_allowable_link_id`. This range should include all the possible values of nodes and links that may be used in your travel model. The software will fail with an error message if a Project Card with an `model_node_id` or `model_link_id` that is outside these allowable ranges.  
3. Next, also in the `registry_config.yml` file, we need to define the node and link identifiers that are already used in the base network that the Project Cards are being applied to. These can be generic to the entire region, or specific to geographies, such as counties. This accommodates configurations, such as the one used by the Metropolitan Transportation Commission, in which node and link ranges are segmented by county. For each geography, the user must define the `start` and `end` nodes and links that are used in the base year network. The software will fail with an error message if a Project Card introduces a `model_node_id` or `model_link_id` that is already used by the base network.  
4. Add a Project Card to the `projects` directory. Commit the change to GitHub. That's it.

## How Does this Work?
When a Project Card is added to the `projects` directory and committed to GitHub, the repository runs a set of procedures to do the following:
1. Identify Project Cards that add roadway or transit links to the network.
2. Fail if the Project Card adds a node or link with an ID that is already in the base network, as this suggest their may be a disconnect between the configuration file and the details of the base network. 
3. Update the `registry.csv` database with the new nodes and/or new links, identifying the project that adds them.
4. If a Project Card that adds links conflicts with nodes or links identified in the `registry.csv` database, these nodes and links are updated to use a node or link number that is not in the registry. The Project Cards are updated accordingly.
