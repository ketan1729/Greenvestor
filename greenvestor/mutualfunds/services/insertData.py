from datetime import datetime
import json
from ..models import *

from dateutil import parser


# Function to convert string to datetime
def convert(date_time):
    try:
        if type(date_time) == str:
            return parser.parse(date_time)
        elif type(date_time) == int:
            return datetime.fromtimestamp(date_time / 1e3)
    except:
        return datetime.now()
    return datetime.now()


def populateFund(record):
    fund = Fund()
    fund.symbol = record['fund_symbol']
    fund.short_name = record['fund_short_name']
    fund.long_name = record['fund_long_name']
    fund.category = record['fund_category']
    fund.family = record['fund_family']
    fund.inception_date = convert(record['inception_date'])
    fund.management_name = record['management_name']
    fund.management_bio = record['management_bio']
    fund.investment_strategy = record['investment_strategy']
    fund.management_start_date = convert(record['management_start_date'])
    fund.fund_yield = float(record['fund_yield'])
    fund.yeartodate_return = float(record['year_to_date_return'])
    return fund


def populateAsset(record, fund):
    asset = Asset()
    asset.fund = fund
    asset.total = int(record['total_net_assets'])
    asset.cash = float(record['asset_cash'])
    asset.stocks = float(record['asset_stocks'])
    asset.bonds = float(record['asset_bonds'])
    asset.others = float(record['asset_others'])
    asset.preferred = float(record['asset_preferred'])
    asset.convertible = float(record['asset_convertible'])
    return asset


def populateReturns(record, fund):
    obj_list = []
    for key in record:
        if not key.startswith("fund_return_2"):
            continue

        if "q" not in key:
            continue

        ret_obj = Returns()
        ret_obj.fund = fund

        year = int(key[key.index("2"):key.index("2") + 4])
        quarter = int(key[-1])
        ret_obj.year = year
        ret_obj.quarter = quarter
        ret_obj.value = float(record[key])

        obj_list.append(ret_obj)

    return obj_list


def populateEsg(record, fund):
    esg = Esg()
    esg.fund = fund

    esg.peer_count = int(record['esg_peer_count'])
    esg.peer_group = record['esg_peer_group']

    esg.esg_score = float(record['esg_score'])
    esg.peer_esg_min = float(record['peer_esg_min'])
    esg.peer_esg_avg = float(record['peer_esg_avg'])
    esg.peer_esg_max = float(record['peer_esg_max'])

    esg.env_score = float(record['environment_score'])
    esg.peer_env_min = float(record['peer_environment_min'])
    esg.peer_env_avg = float(record['peer_environment_avg'])
    esg.peer_env_max = float(record['peer_environment_max'])

    esg.soc_score = float(record['social_score'])
    esg.peer_soc_min = float(record['peer_social_min'])
    esg.peer_soc_avg = float(record['peer_social_avg'])
    esg.peer_soc_max = float(record['peer_social_max'])

    esg.gov_score = float(record['governance_score'])
    esg.peer_gov_min = float(record['peer_governance_min'])
    esg.peer_gov_avg = float(record['peer_governance_avg'])
    esg.peer_gov_max = float(record['peer_governance_max'])

    return esg


def populateOther(record, fund):
    obj_list = []
    col_list = ['3years', '5years', '10years']

    for col in col_list:
        other = Other()
        other.fund = fund
        other.years = int(col[0:col.index("y")])
        other.alpha = float(record['fund_alpha_' + col])
        other.beta = float(record['fund_beta_' + col])
        other.mean_annual_return = float(record['fund_mean_annual_return_' + col])
        other.r_squared = float(record['fund_r_squared_' + col])
        other.std_dev = float(record['fund_stdev_' + col])
        other.sharpe_ratio = float(record['fund_sharpe_ratio_' + col])
        other.treynor_ratio = float(record['fund_treynor_ratio_' + col])
        obj_list.append(other)

    return obj_list


def populateSector(record, fund):
    sector = Sector()
    sector.fund = fund
    sector.basic_materials = float(record['fund_sector_basic_materials'])
    sector.comm_services = float(record['fund_sector_communication_services'])
    sector.consumer_cyclical = float(record['fund_sector_consumer_cyclical'])
    sector.consumer_defensive = float(record['fund_sector_consumer_defensive'])
    sector.energy = float(record['fund_sector_energy'])
    sector.financial_services = float(record['fund_sector_financial_services'])
    sector.healthcare = float(record['fund_sector_healthcare'])
    sector.industrials = float(record['fund_sector_industrials'])
    sector.real_estate = float(record['fund_sector_real_estate'])
    sector.technology = float(record['fund_sector_technology'])
    sector.utilities = float(record['fund_sector_utilities'])
    return sector


def insertData():
    path = 'D:\\Rutgers\\Acads\\SE\\Project\\Data\\mutualfunds.json'

    with open(path) as json_file:
        data = json.load(json_file)
        count = 0
        for record in data:
            fund = populateFund(record)
            fund.save()

            asset = populateAsset(record, fund)
            asset.save()

            returns_obj_list = populateReturns(record, fund)
            for ret_obj in returns_obj_list:
                ret_obj.save()

            esg = populateEsg(record, fund)
            esg.save()

            other_obj_list = populateOther(record, fund)
            for other_obj in other_obj_list:
                other_obj.save()

            sector = populateSector(record, fund)
            sector.save()

            count += 1
            print("Record number " + str(count) + " done")

# if __name__ == '__main__':
#     insertData()
