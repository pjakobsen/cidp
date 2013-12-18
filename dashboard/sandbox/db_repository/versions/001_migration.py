from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
activity = Table('activity', pre_meta,
    Column('activity_id', BigInteger, nullable=False),
    Column('project_num', String),
    Column('project_number', Text),
    Column('hierarchy', BigInteger),
    Column('last-updated-datetime', DateTime),
    Column('default-language', DateTime),
    Column('reporting-org', DateTime),
    Column('reporting-org-ref', String),
    Column('reporting-org-type', String),
    Column('title', String),
    Column('description', String),
    Column('activity-status-code', BigInteger),
    Column('start-planned', DateTime),
    Column('end-planned', DateTime),
    Column('start-actual', DateTime),
    Column('end-actual', DateTime),
    Column('participating-org (Accountable)', DateTime),
    Column('participating-org-ref (Accountable)', DateTime),
    Column('participating-org-type (Accountable)', DateTime),
    Column('participating-org (Funding)', String),
    Column('participating-org-ref (Funding)', String),
    Column('participating-org-type (Funding)', String),
    Column('participating-org (Extending)', String),
    Column('participating-org-ref (Extending)', String),
    Column('participating-org-type (Extending)', String),
    Column('participating-org (Implementing)', String),
    Column('participating-org-ref (Implementing)', BigInteger),
    Column('participating-org-type (Implementing)', String),
    Column('recipient-country-code', String),
    Column('recipient-country', String),
    Column('recipient-country-percentage', String),
    Column('recipient-region-code', BigInteger),
    Column('recipient-region', String),
    Column('recipient-region-percentage', String),
    Column('sector-code', String),
    Column('sector', String),
    Column('sector-percentage', String),
    Column('sector-vocabulary', String),
    Column('collaboration-type-code', BigInteger),
    Column('default-finance-type-code', BigInteger),
    Column('default-flow-type-code', BigInteger),
    Column('default-aid-type-code', String),
    Column('default-tied-status-code', DateTime),
    Column('default-currency', String),
    Column('currency', DateTime),
    Column('total-Commitment', BigInteger),
    Column('total-Disbursement', BigInteger),
    Column('total-Expenditure', BigInteger),
    Column('total-Incoming Funds', BigInteger),
    Column('total-Interest Repayment', BigInteger),
    Column('total-Loan Repayment', BigInteger),
    Column('total-Reimbursement', BigInteger),
)

cida = Table('cida', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('fiscal_year', Text),
    Column('project_number', Text),
    Column('status', Text),
    Column('maximum_cida_contribution', Float),
    Column('branch_id', Text),
    Column('branch_name', Text),
    Column('division_id', Text),
    Column('division_name', Text),
    Column('section_id', Text),
    Column('section_name', Text),
    Column('regional_program', Text),
    Column('fund_centre_id', Text),
    Column('fund_centre_name', Text),
    Column('untied_amount', Float),
    Column('fstc_percent', Text),
    Column('irtc_percent', Text),
    Column('cfli', Text),
    Column('cida_business_delivery_model', String),
    Column('bilateral_aid', Text),
    Column('pba_type', Text),
    Column('environmental_sustainability', Text),
    Column('climate_change_adaptation', Text),
    Column('climate_change_mitigation', Text),
    Column('desertification', Text),
    Column('participatory_development_and_good_governance', Text),
    Column('trade_development', Text),
    Column('biodiversity', Text),
    Column('urban_issues', Text),
    Column('children_issues', Text),
    Column('youth_issues', Text),
    Column('indigenous_issues', Text),
    Column('disability_issues', Text),
    Column('ict_as_a_tool_for_development', Text),
    Column('knowledge_for_development', Text),
    Column('gender_equality', Text),
    Column('organisation_id', Text),
    Column('organisation_name', Text),
    Column('organisation_type', Text),
    Column('organisation_class', Text),
    Column('organisation_sub_class', Text),
    Column('continent_id', Text),
    Column('continent_name', Text),
    Column('project_browser_country_id', Text),
    Column('country_region_id', Text),
    Column('country_region_name', Text),
    Column('country_region_percent', Text),
    Column('sector_id', Text),
    Column('sector_name', Text),
    Column('sector_percent', Text),
    Column('amount_spent', Float),
    Column('date_modified', Text),
    Column('title', Text),
    Column('description', Text),
    Column('start_date', Text),
    Column('end_date', Text),
    Column('country', Text),
    Column('executing_agency_partner', String),
    Column('cida_sector_of_focus', String),
    Column('dac_sector', Text),
)

country = Table('country', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('country_name', String, nullable=False),
    Column('country_code', String, nullable=False),
    Column('short_name', String),
)

initiative = Table('initiative', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String, nullable=False),
    Column('alternate_name', String, nullable=False),
    Column('short_name', String, nullable=False),
    Column('url', String, nullable=False),
)

initiative_project = Table('initiative_project', pre_meta,
    Column('project_id', Integer, primary_key=True, nullable=False),
    Column('initiative_id', Integer, primary_key=True, nullable=False),
)

project = Table('project', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('project_number', String, nullable=False),
    Column('sub_project_number', String, nullable=False),
    Column('full_project_number', String, nullable=False),
    Column('url', Text, nullable=False),
    Column('project_name', String),
)

projects = Table('projects', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('year', Integer),
    Column('amount', Float),
    Column('continent', String),
    Column('cida_contrib', String),
    Column('org', String),
    Column('status', String),
    Column('br_country_id', String),
    Column('region', String),
    Column('project', String),
    Column('region_percent', String),
    Column('sector', String),
    Column('sector_id', String),
    Column('sector_percent', String),
    Column('browser_title', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['activity'].drop()
    pre_meta.tables['cida'].drop()
    pre_meta.tables['country'].drop()
    pre_meta.tables['initiative'].drop()
    pre_meta.tables['initiative_project'].drop()
    pre_meta.tables['project'].drop()
    pre_meta.tables['projects'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['activity'].create()
    pre_meta.tables['cida'].create()
    pre_meta.tables['country'].create()
    pre_meta.tables['initiative'].create()
    pre_meta.tables['initiative_project'].create()
    pre_meta.tables['project'].create()
    pre_meta.tables['projects'].create()
