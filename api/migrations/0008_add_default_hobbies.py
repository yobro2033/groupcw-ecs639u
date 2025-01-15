from django.db import migrations


def add_default_hobbies(apps, schema_editor):
    """Add default hobbies to the database."""
    Hobbies = apps.get_model('api', 'Hobbies')
    default_hobbies = [
        {'name': 'Reading', 'description': 'Enjoying books and literature'},
        {'name': 'Traveling', 'description': 'Exploring new places and cultures'},
        {'name': 'Cooking', 'description': 'Preparing and experimenting with food'},
        {'name': 'Photography', 'description': 'Capturing moments through camera'},
        {'name': 'Painting', 'description': 'Creating art with colors'},
        {'name': 'Hiking', 'description': 'Walking and exploring nature trails'},
        {'name': 'Gardening', 'description': 'Growing and maintaining plants'},
        {'name': 'Dancing', 'description': 'Moving to music and rhythm'},
        {'name': 'Cycling', 'description': 'Riding bicycles for leisure or sport'},
        {'name': 'Playing musical instruments', 'description': 'Creating music with instruments'}
    ]
    
    for hobby in default_hobbies:
        Hobbies.objects.get_or_create(
            name=hobby['name'],
            defaults={'description': hobby['description']}
        )


def remove_default_hobbies(apps, schema_editor):
    """Remove all hobbies from the database."""
    Hobbies = apps.get_model('api', 'Hobbies')
    Hobbies.objects.all().delete()


class Migration(migrations.Migration):
    """Migration to add default hobbies."""
    
    dependencies = [
        ('api', '0007_alter_user_profile_image'),
    ]

    operations = [
        migrations.RunPython(
            add_default_hobbies,
            remove_default_hobbies
        ),
    ] 