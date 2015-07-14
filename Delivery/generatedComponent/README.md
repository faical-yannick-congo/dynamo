This component is the generated model but will represent the structure of a component.
All the meta components themselves have this structure.
The component is organized in 6 modules.
1-actions: contains the core actions and custom actions that the component can execute.
2-core: contains the core process that represent the instance of the component. It also has the request processor.
3-listen: contains the different set of protocols that the component can use as drivers to instanciate the server.
Note: Not all of them are launched. It depends on the capabilities of the component which is specified is a file later on.
4-requests: contains the timestamped requests received and/or processed.
5-status: contains the configs and used files.
--behavior: behavior determines what will be the state of the component after the reception of a request.
--capability: defines what are the active protocols supported by this component.
--history: contains the history of generation of the component compare to the whole generation process.
--log: contains the summaries log of the component execution.
--mapping: provides where the other components are. It provides what are the different capabilities of each components.
--state: hold the state of the component.
Other: control.sh is the one to run the component. Run it with sudo rights.

To Use this component:
A documentation on the installation of the libs will be provided.
It is a skeleton python, json (hybride: serial, tcp, ip, http, i2c, bluetooth, ir) app that can run a more broad set of actions:(binary, python, perl, ruby, java, scala, pascal, assembly)