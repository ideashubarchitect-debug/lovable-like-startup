# Generated migration: slug, template, published, sections

from django.db import migrations, models


def populate_slugs(apps, schema_editor):
    App = apps.get_model('core', 'App')
    from django.utils.text import slugify
    used = set()
    for app in App.objects.all():
        base = slugify(app.name) if app.name else f'app-{app.pk}'
        if not base:
            base = 'app'
        slug = base
        idx = 1
        while slug in used:
            slug = f'{base}-{idx}'
            idx += 1
        used.add(slug)
        app.slug = slug
        app.save(update_fields=['slug'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='slug',
            field=models.SlugField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='app',
            name='template',
            field=models.CharField(
                choices=[('landing', 'Landing Page'), ('saas', 'SaaS / Product'), ('portfolio', 'Portfolio')],
                default='landing',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='app',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='app',
            name='sections',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(populate_slugs, noop),
        migrations.AlterField(
            model_name='app',
            name='slug',
            field=models.SlugField(blank=True, max_length=80, unique=True),
        ),
    ]
