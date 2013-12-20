multilateral_contributions = {   
        'gavi':{'name':'GAVI','imputed':100},
        'aids':{'name':'Global Fund to Fight AIDS, TB and Malaria','imputed':46},
        'AfDF':{'name':'Regional Development Banks AfDF','imputed':3},
        'AsDF':{'name':'Regional Development Banks  AsDF','imputed':2},
        'idb':{'name':'Regional Development Banks IDB Special Fund','imputed':1},
        'unfpa':{'name':'UNFPA','imputed':67},
        'unicef':{'name':'UNICEF','imputed':55},
        'wb':{'name':'World Bank','imputed':5},
        'wfp':{'name':'World Food Programme','imputed':15},
        'who':{'name':'World Health Organization','imputed':22}
    }
  
#Calculations amounts
calcs=[value['imputed'] for value in multilateral_contributions.values()]


#Bilateral contributions
#code','name','imputed
bilateral_contributions=[('12110','Health policy and administrative management','40%'),
('12181','Medical education/training','40%'),
('12191','Medical services','40%'),
('12220','Basic health care','40%'),
('12230','Basic health infrastructure','40%'),
('12240','Basic nutrition','100%'),
('12250','Infectious disease control','40%'),
('12261','Health education','40%'),
('12262','Malaria control','88.5%'),
('12263','Tuberculosis control','18.5%'),
('12281','Health personnel development','40%'),
('13010','Population policy and administrative management','40%'),
('13020','Reproductive health care','100%'),
('13030','Family planning','100%'),
('13040','STD control including HIV/AIDS','46.1%'),
('13081','Personnel development for population and reproductive health','100%'),
('14030','Basic drinking water supply and basic sanitation','15%'),
('14031','Basic drinking water supply','15%'),
('14032','Basic sanitation','15%'),
('51010','General budget support','4%')]

bilat=[(b[0],b[2]) for b in bilateral_contributions]



