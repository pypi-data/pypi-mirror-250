### Genmax

Genmax is a simple code generation tool.

#### Key Components

- Projects

Genmax organizes all files and content in projects. Every project has itown folder. Genmax projects can be created in any folder.

- Flows

Genmax projects have flows to group together multiple files to be generated. Flows are in **yml** format.

- Data

You can pass data to templates that help generate data. For example, you can dynamically pass the name of attributes if you are generating a class file.

- Templates

These templates form the basis of the code to be generated. Genmax uses the Jinja2 engine for code generation.

- Output

Once the data is passed to a template, Genmax generates an output file with the generated code. For nested output locations, you can use **>** as a separator.

#### Commands

| Command | Description |
|:---|:---|
|gmx add proj \<project-name> | Create a new project.|
|gmx set proj \<project-name> | Set the current project.|
|gmx wf run \<workflow-name> | Run workflow for a given project.|

#### Extensions supported in templates

The following methods are supported in the template:

| Description | Method |
|:---|:---|
|Lower case| lcase(your_string)|
|Pluralize| pluralize(your_string)|
|Join With Commas| joinify(name_of_element, element_list)|
|Switch to Camel case| camel(your_string)|
|Switch to Kebab case| kebab(your_string)|
|Switch to Pascale case| pascale(your_string)|
|Switch to Dot case| dot(your_string)|
|Switch to Title case| title(your_string)|
|Switch to Snake case| snake(your_string)|
|Switch to Path format| path(your_string)|
|Generate UUID| uuid()|
|Generate secret in 16 bit - hexadecimal| secret()|
|Generate secret in 64 bit - hexadecimal| secret_complex()|

#### Run It

```bash
gmx wf sample sample
```