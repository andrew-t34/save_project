from django import template
from study.models import Program
register = template.Library()


@register.simple_tag
def program_name(program_id=None, program_dict=None):
    if program_id:
        return program_dict[int(program_id)]
    return ''


@register.simple_tag
def get_program_dict():
    program_dict = {}
    programs = Program.objects.all().values('id', 'name')
    for program in programs:
        program_dict[program['id']] = program['name']
    return program_dict

