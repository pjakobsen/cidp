CREATE TABLE crs
(
  "year" VARCHAR(36)
, donorcode BIGINT
, donorname VARCHAR(6)
, agencycode BIGINT
, agencyname VARCHAR(5)
, crsid BIGINT
, projectnumber VARCHAR(33)
, initialreport BIGINT
, recipientcode BIGINT
, recipientname VARCHAR(33)
, regioncode BIGINT
, regionname VARCHAR(23)
, incomegroupcode BIGINT
, incomegroupname VARCHAR(28)
, flowcode BIGINT
, flowname VARCHAR(10)
, bi_multi BIGINT
, category BIGINT
, finance_t BIGINT
, aid_t VARCHAR(3)
, usd_commitment VARCHAR(21)
, usd_disbursement VARCHAR(22)
, usd_received VARCHAR(21)
, usd_commitment_defl VARCHAR(21)
, usd_disbursement_defl VARCHAR(22)
, usd_received_defl VARCHAR(21)
, usd_adjustment VARCHAR(22)
, usd_adjustment_defl VARCHAR(22)
, usd_amountuntied VARCHAR(21)
, usd_amountpartialtied VARCHAR(21)
, usd_amounttied VARCHAR(22)
, usd_amountuntied_defl VARCHAR(21)
, usd_amountpartialtied_defl VARCHAR(21)
, usd_amounttied_defl VARCHAR(22)
, usd_IRTC VARCHAR(22)
, usd_expert_commitment TIMESTAMP
, usd_expert_extended TIMESTAMP
, usd_export_credit BIGINT
, currencycode BIGINT
, commitment_national VARCHAR(21)
, disbursement_national VARCHAR(22)
, shortdescription VARCHAR(162)
, projecttitle VARCHAR(207)
, purposecode BIGINT
, purposename VARCHAR(59)
, sectorcode BIGINT
, sectorname VARCHAR(49)
, channelcode BIGINT
, channelname VARCHAR(102)
, channelreportedname VARCHAR(110)
, geography VARCHAR(100)
, expectedstartdate TIMESTAMP
, completiondate TIMESTAMP
, longdescription VARCHAR(4134)
, gender BIGINT
, environment BIGINT
, trade BIGINT
, pdgg BIGINT
, FTC BIGINT
, PBA BIGINT
, investmentproject BIGINT
, assocfinance BIGINT
, biodiversity BIGINT
, climateMitigation BIGINT
, climateAdaptation BIGINT
, desertification BIGINT
, commitmentdate TIMESTAMP
, typerepayment BIGINT
, numberrepayment BIGINT
, interest1 BIGINT
, interest2 BIGINT
, repaydate1 TIMESTAMP
, repaydate2 TIMESTAMP
, grantelement BIGINT
, usd_interest VARCHAR(21)
, usd_outstanding VARCHAR(22)
, usd_arrears_principal VARCHAR(22)
, usd_arrears_interest VARCHAR(21)
, usd_future_DS_principal VARCHAR(22)
, usd_future_DS_interes BIGINT
)
;