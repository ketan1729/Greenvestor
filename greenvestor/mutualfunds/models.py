from django.db import models


# Create your models here.

class Fund(models.Model):
    symbol = models.CharField(max_length=200, default=None)
    short_name = models.CharField(max_length=200)
    long_name = models.CharField(max_length=200, default=None)
    category = models.CharField(max_length=200)
    family = models.CharField(max_length=200, default=None)
    inception_date = models.DateTimeField()
    management_name = models.CharField(max_length=200)
    management_bio = models.TextField()
    investment_strategy = models.TextField()
    management_start_date = models.DateTimeField()
    fund_yield = models.FloatField(default=0.0)
    yeartodate_return = models.FloatField(default=0.0)


class Asset(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    total = models.BigIntegerField()
    cash = models.FloatField(default=0.0)
    stocks = models.FloatField(default=0.0)
    bonds = models.FloatField(default=0.0)
    others = models.FloatField(default=0.0)
    preferred = models.FloatField(default=0.0)
    convertible = models.FloatField (default=0.0)


class Returns(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    quarter = models.IntegerField(default=0)
    value = models.FloatField(default=0.0)


class Esg(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    peer_count = models.IntegerField(default=0)
    peer_group = models.CharField(max_length=200)

    esg_score = models.FloatField(default=0.0)
    peer_esg_min = models.FloatField(default=0.0)
    peer_esg_avg = models.FloatField(default=0.0)
    peer_esg_max = models.FloatField(default=0.0)

    env_score = models.FloatField(default=0.0)
    peer_env_min = models.FloatField(default=0.0)
    peer_env_avg = models.FloatField(default=0.0)
    peer_env_max = models.FloatField(default=0.0)

    soc_score = models.FloatField(default=0.0)
    peer_soc_min = models.FloatField(default=0.0)
    peer_soc_avg = models.FloatField(default=0.0)
    peer_soc_max = models.FloatField(default=0.0)

    gov_score = models.FloatField(default=0.0)
    peer_gov_min = models.FloatField(default=0.0)
    peer_gov_avg = models.FloatField(default=0.0)
    peer_gov_max = models.FloatField(default=0.0)


class Other(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    years = models.IntegerField(default=0)
    alpha = models.FloatField(default=0.0)
    beta = models.FloatField(default=0.0)
    mean_annual_return = models.FloatField(default=0.0)
    r_squared = models.FloatField(default=0.0)
    std_dev = models.FloatField(default=0.0)
    sharpe_ratio = models.FloatField(default=0.0)
    treynor_ratio = models.FloatField(default=0.0)


class ExpenseProjection(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class Sector(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    basic_materials = models.FloatField(default=0.0)
    comm_services = models.FloatField(default=0.0)
    consumer_cyclical = models.FloatField(default=0.0)
    consumer_defensive = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    financial_services = models.FloatField(default=0.0)
    healthcare = models.FloatField(default=0.0)
    industrials = models.FloatField(default=0.0)
    real_estate = models.FloatField(default=0.0)
    technology = models.FloatField(default=0.0)
    utilities = models.FloatField(default=0.0)

