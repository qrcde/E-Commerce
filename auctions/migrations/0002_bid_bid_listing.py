# Generated by Django 4.2.17 on 2024-12-11 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listing_bids', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
