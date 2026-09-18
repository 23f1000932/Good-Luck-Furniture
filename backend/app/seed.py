import click
from flask import current_app
from .extensions import db
from .models.admin_user import AdminUser
from .models.category import Category
from .utils.slugify import unique_slug


def register_commands(app):
    """Register CLI commands on the Flask app."""

    @app.cli.command('seed-admin')
    @click.option('--name', prompt='Admin name', help='Admin full name')
    @click.option('--email', prompt='Admin email', help='Admin email address')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
    def seed_admin(name, email, password):
        """Create the initial admin user."""
        existing = AdminUser.query.filter_by(email=email.lower()).first()
        if existing:
            click.echo(f'Admin with email {email} already exists.')
            return

        if len(password) < 8:
            click.echo('Error: Password must be at least 8 characters.')
            return

        admin = AdminUser(
            name=name,
            email=email.lower().strip(),
            role='admin',
            is_active=True,
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo(f'Admin user created: {email}')

    @app.cli.command('seed-categories')
    def seed_categories():
        """Seed default furniture categories."""
        categories = [
            {
                'name': 'Bedroom',
                'description': 'Beds, wardrobes, dressing tables and bedroom storage — complete your personal sanctuary.',
                'display_order': 1,
            },
            {
                'name': 'Living Room',
                'description': 'Sofas, coffee tables, TV units and accent pieces for the heart of your home.',
                'display_order': 2,
            },
            {
                'name': 'Dining Room',
                'description': 'Dining tables, chairs and sideboards crafted for lasting family gatherings.',
                'display_order': 3,
            },
            {
                'name': 'Office',
                'description': 'Study tables, office chairs and storage for a focused, elegant workspace.',
                'display_order': 4,
            },
            {
                'name': 'Home Decor',
                'description': 'Decorative accents, side tables and finishing pieces that complete a room.',
                'display_order': 5,
            },
            {
                'name': 'Custom Furniture',
                'description': 'Bespoke furniture crafted to your exact dimensions, materials and finish.',
                'display_order': 6,
            },
        ]

        count = 0
        for cat_data in categories:
            existing = Category.query.filter_by(name=cat_data['name']).first()
            if existing:
                click.echo(f'Category already exists: {cat_data["name"]}')
                continue

            slug = unique_slug(cat_data['name'], Category)
            category = Category(
                name=cat_data['name'],
                slug=slug,
                description=cat_data['description'],
                display_order=cat_data['display_order'],
                is_active=True,
            )
            db.session.add(category)
            count += 1

        db.session.commit()
        click.echo(f'Seeded {count} categories.')
