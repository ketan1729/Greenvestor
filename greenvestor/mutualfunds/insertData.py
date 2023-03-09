import json
from greenvestor.mutualfunds.models import *


def populateFund(record):
    fund = Fund()
    fund.symbol = record['fund_symbol']
    fund.short_name = record['fund_short_name']
    fund.long_name = record['fund_long_name']
    fund.category = record['fund_category']
    fund.family = record['fund_family']
    fund.inception_date = record['inception_date']
    fund.management_name = record['management_name']
    fund.management_bio = record['management_bio']
    fund.investment_strategy = record['investment_strategy']
    fund.management_start_date = record['management_start_date']
    fund.fund_yield = record['fund_yield']
    fund.yeartodate_return = record['year_to_date_return']
    return fund


def populateAsset(record, fund):
    asset = Asset()
    asset.fund = fund
    asset.total = record['total_net_assets']
    asset.cash = record['asset_cash']
    asset.stocks = record['asset_stocks']
    asset.bonds = record['asset_bonds']
    asset.others = record['asset_others']
    asset.preferred = record['asset_preferred']
    asset.convertible = record['asset_convertible']
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

        year = key[key.index("2"):key.index("2") + 4]
        quarter = key[-1]
        ret_obj.year = year
        ret_obj.quarter = quarter
        ret_obj.value = record[key]

        obj_list.append(ret_obj)

    return obj_list


def populateEsg(record, fund):
    esg = Esg()
    esg.fund = fund

    esg.peer_count = record['esg_peer_count']
    esg.peer_group = record['esg_peer_group']

    esg.esg_score = record['esg_score']
    esg.peer_esg_min = record['peer_esg_min']
    esg.peer_esg_avg = record['peer_esg_avg']
    esg.peer_esg_max = record['peer_esg_max']

    esg.env_score = record['environment_score']
    esg.peer_env_min = record['peer_environment_min']
    esg.peer_env_avg = record['peer_environment_avg']
    esg.peer_env_max = record['peer_environment_max']

    esg.soc_score = record['social_score']
    esg.peer_soc_min = record['peer_social_min']
    esg.peer_soc_avg = record['peer_social_avg']
    esg.peer_soc_max = record['peer_social_max']

    esg.gov_score = record['governance_score']
    esg.peer_gov_min = record['peer_governance_min']
    esg.peer_gov_avg = record['peer_governance_avg']
    esg.peer_gov_max = record['peer_governance_max']

    return esg


def populateOther(record, fund):
    obj_list = []
    col_list = ['3years', '5years', '10years']

    for col in col_list:
        other = Other()
        other.fund = fund
        other.years = int(col[0:col.index("y")])
        other.alpha = record['fund_alpha_' + col]
        other.beta = record['fund_beta_' + col]
        other.mean_annual_return = record['fund_mean_annual_return' + col]
        other.r_squared = record['fund_r_squared' + col]
        other.std_dev = record['fund_stdev' + col]
        other.sharpe_ratio = record['fund_sharpe_ratio' + col]
        other.treynor_ratio = record['fund_treynor_ratio' + col]
        obj_list.append(other)

    return obj_list


def populateSector(record, fund):
    sector = Sector()
    sector.fund = fund
    sector.basic_materials = record['fund_sector_basic_materials']
    sector.comm_services = record['fund_sector_communication_services']
    sector.consumer_cyclical = record['fund_sector_consumer_cyclical']
    sector.consumer_defensive = record['fund_sector_consumer_defensive']
    sector.energy = record['fund_sector_energy']
    sector.financial_services = record['fund_sector_financial_services']
    sector.healthcare = record['fund_sector_healthcare']
    sector.industrials = record['fund_sector_industrials']
    sector.real_estate = record['fund_sector_real_estate']
    sector.technology = record['fund_sector_technology']
    sector.utilities = record['fund_sector_utilities']
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


if __name__ == '__main__':
    insertData()
