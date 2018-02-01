import StringIO
import click

from click_datetime import Datetime
from util import overlay_text_at_loc_on_pdf, make_form_content


@click.group(chain=True)
def cli():
    pass


@click.command()
@click.argument('employee', type=str)
@click.argument('manager', type=str)
@click.argument('num_days', type=int)
@click.argument('from_date', type=Datetime(format='%d/%m/%y'))
@click.argument('to_date', type=Datetime(format='%d/%m/%y'))
@click.option('--output-file', type=click.Path(exists=False),
              default='holiday_request.pdf')
@click.option('--template-file', type=click.Path(exists=True),
              default='holidays.pdf')
@click.pass_context
def holiday(ctx, employee, manager, num_days, from_date,
            to_date, output_file, template_file):
    """
    Holidays for the lazy.

    Fills out a holiday request form on your behalf so you don't have to.
    """
    text_and_locs = make_form_content(employee, manager, num_days, from_date.strftime(
        '%d/%m/%y'), to_date.strftime('%d/%m/%y'))
    overlay_text_at_loc_on_pdf(text_and_locs, template_file, output_file)
    ctx.obj['output_file'] = output_file

@click.command()
@click.option('--form-file', default='holiday_request.pdf')
@click.pass_context
def inspect(ctx, form_file):
    """
    Open a filled out PDF form for your holidays
    """
    from subprocess import call
    file_to_open = ctx.obj.get('output_file') or form_file
    click.echo("Opening {}".format(file_to_open))
    call(["open", file_to_open])


@click.command()
@click.pass_context
@click.argument('address', type=str)
def email(ctx, address):
    """
    Send to your manager
    """
    click.echo("Sending to {}".format(address))

cli.add_command(holiday)
cli.add_command(inspect)
cli.add_command(email)


if __name__ == '__main__':
    cli(obj={})
