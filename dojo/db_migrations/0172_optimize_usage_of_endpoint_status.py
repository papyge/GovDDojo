# Generated by Django 3.2.13 on 2022-04-26 20:44

from django.db import migrations, models
import dojo.models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0171_jira_labels_per_product_and_engagement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endpoint',
            name='endpoint_status',
        ),
        migrations.RemoveField(
            model_name='finding',
            name='endpoint_status',
        ),
        # Yes, we can just remove it and add it again because there reduntant data in "Endpoint_Status" - there will be no data-loss; it was tested
        # AlterField is not usable because of: ValueError: Cannot alter field xxx into yyy - they are not compatible types (you cannot alter to or from M2M fields, or add or remove through= on M2M fields)
        migrations.RemoveField(
            model_name='finding',
            name='endpoints',
        ),
        migrations.AddField(
            model_name='finding',
            name='endpoints',
            field=models.ManyToManyField(blank=True,
                                         help_text='The hosts within the product that are susceptible to this flaw. + The status of the endpoint associated with this flaw (Vulnerable, Mitigated, ...).',
                                         through='dojo.Endpoint_Status',
                                         to='dojo.Endpoint',
                                         verbose_name='Endpoints'),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='findings',
            field=models.ManyToManyField(blank=True,
                                         through='dojo.Endpoint_Status',
                                         to='dojo.Finding',
                                         verbose_name='Findings'),
        ),
        migrations.AlterField(
            model_name='endpoint_status',
            name='date',
            field=models.DateField(default=dojo.models.get_current_date),
        ),
    ]
