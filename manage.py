#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import ast
import sys
from django.conf import settings

# import ptvsd
# ptvsd.enable_attach(address=('0.0.0.0', 5678))

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoreRoot.settings')
    print(os.environ.get('PTVSD_PORT'))
    # Get the value of RUN_IN_DOCKER from the environment variable and default to False
    run_in_docker = ast.literal_eval(os.environ.get('RUN_IN_DOCKER', 'False'))
    print(os.environ.get('RUN_IN_DOCKER'))  
    print(run_in_docker) 
    if run_in_docker: 
        import ptvsd
        port  = int(os.environ.get('PTVSD_PORT'))
        print(port)
        ptvsd.enable_attach(address=('0.0.0.0', os.environ.get('PTVSD_PORT')), redirect_output=True)
        print('ptvsd attached')
    else:
        print('ptvsd not attached')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
