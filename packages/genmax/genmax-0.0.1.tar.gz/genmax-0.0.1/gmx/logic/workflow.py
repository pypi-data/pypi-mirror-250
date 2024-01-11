import os
import sys
import yaml
import gmx.extensions as ex
from jinja2 import Environment, FileSystemLoader

class WorkFlowLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_items(project_name, items):
        # Set up the Jinja2 environment
        env = Environment(loader=FileSystemLoader(os.path.join(project_name, 'templates')))
        env.globals['lcase'] = ex.lcase
        env.globals['joinify'] = ex.joinify
        env.globals['pluralize'] = ex.pluralize
        env.globals['camel'] = ex.camel
        env.globals['kebab'] = ex.kebab
        env.globals['pascale'] = ex.pascale
        env.globals['dot'] = ex.dot
        env.globals['title'] = ex.title
        env.globals['snake'] = ex.snake
        env.globals['path'] = ex.path
        env.globals['uuid'] = ex.uuid
        env.globals['secret'] = ex.secret
        env.globals['secret_complex'] = ex.secret_complex
        # Loop through the items and generate the output files
        for item in items:
            # Load the source data
            try:
                data_path = os.path.join(project_name, 'data', item['data'])
                with open(
                    data_path
                    ) as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)                
            except:
                print(f'Error reading {data_path}.')

            # Load the template
            template = env.get_template(item['template'])

            # Render the template with the source data
            output = template.render(data=data)

            # Save the output tot the specified output file
            output_path = os.path.join(project_name, 'output', item['output'])
            try:
                with open(
                    output_path,
                    'w'
                    ) as f:
                    f.write(output)
            except:
                print(f'Error writing output {output_path}')

    @staticmethod
    def run_workflows(project_name: str, flows: list):
        for flow in flows:
            project_name = os.path.join('projects', project_name)
            flow_path = os.path.join(project_name, 'flows', f'{flow}.yml')
            print(f'Processing Flow : {flow_path}.')
            # Load the items from the YAMl file
            try:
                with open(
                        flow_path
                    ) as f:
                    items = yaml.safe_load(f)
                    WorkFlowLogic.process_items(project_name, items)
                print(f'Flow Status: Done.\n')
            except Exception as e: 
                print(f'Flow processing failed.')
                print(f'Check Flow YAMl and filename(s).')
                continue

