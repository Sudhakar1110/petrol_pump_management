"""Workspace setup helper - calls setup.create_workspace().
Run via: bench --site <site> execute petrol_pump_management.workspace_setup
"""
from petrol_pump_management.setup import create_workspace


def execute():
    create_workspace()
