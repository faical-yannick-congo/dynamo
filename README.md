# DynamicDerivation
Generation of distributed components from requirements specification.
Major components are:
- GlobalSysComponent: In charge of parsing the expression and communicating with the other components to create, destroy or update the generated components.
- MetaBehavComponent: In charge of handling the behavior of the components. Firing up the distributed architecture and handling its behavior.
- MetaStructComponent: In charge of handling the structure of the components.