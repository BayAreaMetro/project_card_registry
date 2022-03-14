# Project Card Registry 
A registry for Network Wrangler Project Cards.

[Network Wrangler 2.0](https://github.com/wsp-sag/network_wrangler) is a Python library for managing travel model network scenarios. Network Wrangler uses `Project Cards` to define network edits. The purpose of this repository is to automate the reconciliation of conflicting Project Cards.

Consider, for example, an existing base year network that includes nodes A, B, and C. Project Card X extends Main Street, adding Node 1 at Location Alpha. Project Card Y extends Broad Street, adding a different node at Location Beta, but also labeling the new node Node 1. In the current Network Wrangler framework, users must manually manage the conflicting `Node 1` definitions. The purpose of this repository is to automate the node (and link) numbering process via a registry.

## Instructions
1. To get started, open up the `registry_config.yml` file in a text editor. This file defines the allowable range of the `model_node_id` and `model_link_id` fields using the `minimum_allowable_node_id`, `maximum_allowable_node_id`, `minimum_allowable_link_id` and `maxmimum_allowable_link_id`. This range should include all the possible values of nodes and links that may be used in your travel model. The software will fail with an error message if a Project Card with an `model_node_id` or `model_link_id` that is outside these allowable ranges.  
2. Next, also in the `registry_config.yml` file, we need to define the node and link identifiers that are already used in the base network that the Project Cards are being applied to. These can be generic to the entire region, or specific to geographies, such as counties. This accommodates configurations, such as the one used by the Metropolitan Transportation Commission, in which node and link ranges are segmented by county. For each geography, the user must define the `start` and `end` nodes and links that are used in the base year network. The software will fail with an error message if a Project Card introduces a `model_node_id` or `model_link_id` that is already used by the base network.  
3. Add a Project Card to the `projects` directory (or in a sub-folder of the `projects` directory). Commit the change to GitHub. That's it.

## How Does this Work?
When a Project Card is added to the `projects` directory and committed to GitHub, the repository runs a set of procedures to do the following:
1. Identify Project Cards that add roadway or transit links to the network.
2. Fail if the Project Card adds a node or link with an ID that is already in the base network, as this suggest their may be a disconnect between the configuration file and the details of the base network. 
3. Update the `registry.csv` database with the new nodes and/or new links, identifying the project that adds them.
4. If a Project Card that adds links conflicts with nodes or links identified in the `registry.csv` database, these nodes and links are updated to use a node or link number that is not in the registry. The Project Cards are updated accordingly.

### Removing a Project Card from the Registry
To remove a Project Card from the registry, a user must do the following:
1. Check out repository.
2. Open the `registry.csv` database in a text editor and delete the entries specific to the project we want to remove.
3. Delete the project card from the `projects` directory. 
4. Commit the change to GitHub.

### Editing a Project Card already entered to the Registry
Once a Project Card has been added to the registry, a user must do the following:
1. Check out the repository.
2. Open the `registry.csv` database in a text editor and delete the entries specific to the project we want to remove.
3. Edit the subject Project Card.
4. Commit the change to GitHub.

### Dependicies Across Project Cards
The registry software currently treats each Project Card independently. As such, if one Project Card adds a link and a second Project Card modifies the attribute of that link, the user is responsible to make sure the `model_link_id`s across the two cards align. To do this, we recommend:
1. First create the Project Card to add the desired nodes and links.
2. Upload this Project Card so that the nodes and link identifiers are registered in the registry and the Project Cards are updated. 
3. Use the node and link identifiers in the registry for subsequent Project Cards that modify the attributes of these new node and links. 

### Tips for Coding Projects
When using the Project Card registry, using these tricks will make things easier:
1. When creating a new roadway link, use the same `model_link_id` for each new link. Specifically, use the number that is one larger than the `end` value used in each county as defined in the `registry_config.yml`. For example, the `end` value used in San Francisco County is `133492`. Each new link added in San Francisco County should then have a `model_link_id` of `133493`. When Project Cards with this `model_link_id` are uploaded to this registry, the software will update the `model_link_id` to the next available number. 
2. Similar to the above approach, when a new node is added, the user should use the next available node number per the county-specific rules. For example, a network node added in Sonoma County should use `4556146`, because the `end` network value used in the base network is `4556145`. If more than one node is added in a single Project Card, each should be incremented from one, starting with the next available number.
3. Network Wrangler allows you to have two types of Project Cards: `.yml` files or `.wrangler` files. The `.yml` file require a certain structure and allow users to implement proscribed procedures for editing the network. The `.wrangler` files allow the user to write Python code directly to modify the network. The registry only acts on the `.yml` files, not the `.wrangler` files. Nodes and links should not be added via `.wrangler` cards for this reason. 

