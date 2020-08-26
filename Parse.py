import re
import pandas as pd
import numpy as np
from dateutil import parser
from tabulate import tabulate


_rx_dict = {
    re.compile(r'(.*?)\|credit\.creditBureau\.creditData\[(\d+)\]\.(.*)\|(.*?)\s*$'):'CREDITBUREAU',
    re.compile(r'(.*?)\|sourceData\.behaviourData\.persons\[(\d+)\]\.(.*)\|(.*?)\s*$'):'BEHAVIOURDATA',
    re.compile(r'(.*?)\|applicantData\.previousApplications\.persons\[(\d+)\]\.(.*)\|(.*?)\s*$'):'PREVAPPLICATION',
    re.compile(r'(.*?)\|documents\[(\d+)\]\.(.*)\|(.*?)\s*$'):'DOCUMENTS',
    re.compile(r'(.*?)\|persons\[(\d+)\]\.(\w*)\|(.*?)\s*$'):'PERSONS',
    re.compile(r'(.*?)\|(.\w*)\|(.*?)\s*$'):'APPLICATION',
    re.compile(r'(.*?)\|predictorsList\[(\d+)\]\.(.*)\|(.*?)\s*$'):'PREDICTORSLIST',
    re.compile(r'(.*?)\|approvalCharacteristics\[(\d+)\]\.(.*)\|(.*?)\s*$'):'PREDICTORSCASH',
    re.compile(r'(.*?)\|(idCredit)\|(.*?)\s*$'):'SK_APPLICATION'
}


_df_dict  = {
    'CREDITBUREAU':[],
    'BEHAVIOURDATA':[],
    'APPLICATION':[],
    'PREVAPPLICATION':[],
    'DOCUMENTS':[],
    'PERSONS':[],
    'PREDICTORSCASH':[],
    'PREDICTORSLIST':[],
    'SK_APPLICATION':[]
}


def set_vct_data_type(p_list):

    if len(p_list) == 3:
        p_list.insert(1,0)

    p_list[2] = p_list[2].upper()

    if p_list[0]=='d':
        p_list[3] = parser.parse(p_list[3],dayfirst=True)
    elif p_list[0]=='n' and p_list[2]=='IDCREDIT':
        p_list[3] = int(p_list[3])
    elif p_list[0]=='n':
        p_list[3] = float(p_list[3])    
    else:
        p_list[3] = str(p_list[3])
    pass    


def parse_vct(p_input,p_dict=_df_dict,p_rx_dict=_rx_dict):

    v_dict = p_dict

    with open(p_input,encoding='utf-8') as file:
        line = file.readline()
        while line:

            for rx,val in p_rx_dict.items():

                if re.search(rx, line):
                    #make list from line
                    temp_list = list(re.findall(rx,line)[0])
                    #set data types
                    set_vct_data_type(temp_list)
                    #append list element to dictionary 
                    v_dict[val].append(temp_list)

            line = file.readline()

    return v_dict

def parse_vct_str(p_input,p_dict=_df_dict,p_rx_dict=_rx_dict):

    v_dict = p_dict

    for line in p_input.split('\n'):
        
        for rx,val in p_rx_dict.items():

            if re.search(rx, line):
                #make list from line
                temp_list = list(re.findall(rx,line)[0])
                #set data types
                set_vct_data_type(temp_list)
                #append list element to dictionary 
                v_dict[val].append(temp_list)

    return v_dict      

def get_df_vct_blaze(p_type,p_dict):

    df = pd.DataFrame(p_dict[p_type])
    #get columns name

    if not df.empty:

        column = df[2].unique()
        #unstack and clean dataframe
        df = df.drop(0,1).set_index([1, 2]).unstack().droplevel(0, axis=1).rename_axis(
            index=None, columns=None).reindex(column, axis=1)
        df['SK_APPLICATION'] = p_dict['SK_APPLICATION'][0][3]

    elif p_type!='PREDICTORSCASH':

        df = df.append({'SK_APPLICATION': p_dict['SK_APPLICATION'][0][3]},ignore_index=True)
        #print(df)

    return df



test_str = '''
c|applicantData.bankAccountBankCode|2291
n|applicantData.bankAccountOwner|0
n|applicantData.creditLimit.creditTypeRange|0
n|applicantData.creditLimit.guarantedLimit|0
c|applicantData.creditTypePrefered|0
c|applicantData.productRequested|POS;SHOPPING_CARD
c|applicantData.typeProcess|isProcess=>Pos5Fields;isTypeApplication=>Short;PDN_Process
n|applicantData.expense.persons[0].cuid|60268391
n|applicantData.previousApplications.isTwPartnerLimitAvailable|0
n|applicantData.previousApplications.persons[0].FZcnt|0
n|applicantData.previousApplications.persons[0].cntContractActiveCar|0
n|applicantData.previousApplications.persons[0].cntContractActiveCash|0
n|applicantData.previousApplications.persons[0].cntContractActivePos|0
n|applicantData.previousApplications.persons[0].cntContractActiveRevolving|0
n|applicantData.previousApplications.persons[0].cntContractActiveRevolvingHomer|0
n|applicantData.previousApplications.persons[0].cntContractActiveRevolvingTW|0
n|applicantData.previousApplications.persons[0].cntContractActiveRevolvingTWPolza|0
n|applicantData.previousApplications.persons[0].cuid|60268391
d|applicantData.previousApplications.persons[0].lastMobilePhoneChangeDate|14.05.2020 16:02:21
c|application.signMethodOptions|SMS_SIGN, SIGN_DBO, PERSONAL
c|application.signMethodSelected|PERSONAL
c|credit.KMBCard|0
n|credit.accountStatement|0
n|credit.avgPartnerTerm|12
n|credit.avgRevTerm|1
n|credit.cashOnNncLimit|0
n|credit.coefDualRDLimitUse|1
n|credit.creditAmount|0
n|credit.creditAmountNext|0
n|credit.creditAmountPrevious|0
c|credit.creditType|SS
d|credit.dateReview|14.05.2020 16:02:20
n|credit.deferredPayments|0
n|credit.flexiPaymentNumReduction|0
n|credit.initPay|0
n|credit.insurancePremium|0
c|credit.insurancePremiumExist|0
n|credit.insurancePremiumGoods|0
c|credit.insurancePremiumGoodsExist|0
n|credit.insurancePremiumUnemp|0
c|credit.insurancePremiumUnempExist|0
n|credit.isDynamic|0
n|credit.isFinalBasket|0
n|credit.isMultiSelect|0
n|credit.isPosOnCard|1
n|credit.isPseudo|0
n|credit.isTW|0
n|credit.lostThingsFeeAmount|0
c|credit.mfo|bank
n|credit.monthlyFeeDebt|0
n|credit.photoExists|1
n|credit.refinCashCreditAmount|0
n|credit.scansAttached|0
n|credit.scansChanged|0
c|credit.scoringTypeCode|OLD_SCORING_TYPE
n|credit.secondInterestRateType|0
c|credit.typeSp|8
n|credit.creditProduct.scansMinSum|0
n|credit.creditProduct.scansRequired|0
n|credit.persons[0].cuid|60268391
c|documents[0].cardNumber|7*********
n|documents[0].cardOrder|1
n|documents[0].cuid|60268391
c|documents[0].groupNumber|1
c|documents[0].identCardType|pass
c|documents[0].personType|1
c|documents[0].placeOfIssue|ОТДЕЛЕНИЕМ УФМС РОССИИ ПО ЯРОСЛАВСКОЙ ОБЛАСТИ В ГОРОДЕ ТУТАЕВЕ И ТУТАЕВСКОМ РАЙОНЕ
d|documents[0].published|03.02.2009 00:00:00
c|documents[0].specification|760-022
c|personContact[0].contact|9807460233
n|personContact[0].cuid|60268391
n|personContact[0].order|1
c|personContact[0].personType|1
c|personContact[0].relationShipToClient|itself
c|personContact[0].type|16
c|personContact[1].contact|9807460233
n|personContact[1].cuid|60268391
n|personContact[1].order|1
c|personContact[1].personType|1
c|personContact[1].relationShipToClient|itself
c|personContact[1].type|2
c|personContact[2].contact|Andrey6464@mail.ru
n|personContact[2].cuid|60268391
n|personContact[2].order|1
c|personContact[2].personType|1
c|personContact[2].relationShipToClient|itself
c|personContact[2].type|4
n|persons[0].activeRdOffer|0
n|persons[0].activeScOffer|0
d|persons[0].birth|02.01.1964 00:00:00
c|persons[0].birthPlace|ПОС ЧИСТОЕ ЧКАЛОВСКОГО РНА НИЖЕГОРОДСКОЙ ОБЛ
c|persons[0].contactMobilePhone|980*****33
n|persons[0].cuid|60268391
c|persons[0].email|Andrey6464@mail.ru
c|persons[0].ident|78******48
c|persons[0].incomeType|c
n|persons[0].isFakeCuid|0
c|persons[0].isNewApplicant|new
n|persons[0].mainOccupationIncome|25000
c|persons[0].mobil|9807460233
c|persons[0].name1|А*****
c|persons[0].name2|Н********
c|persons[0].nameMid|Н*********
c|persons[0].occupation|пенсионер
c|persons[0].personType|1
n|persons[0].personUndesirable|0
c|persons[0].registeredAddress.apartmentNumber|180
c|persons[0].registeredAddress.district|Тутаевский
c|persons[0].registeredAddress.districtCode|016
c|persons[0].registeredAddress.districtType|р-н
n|persons[0].registeredAddress.floorsMax|9
c|persons[0].registeredAddress.localityCode|000
c|persons[0].registeredAddress.localityType|г
c|persons[0].registeredAddress.region|76
c|persons[0].registeredAddress.regionName|Ярославская
c|persons[0].registeredAddress.regionType|обл
c|persons[0].registeredAddress.standard|s
c|persons[0].registeredAddress.street|Дементьева
c|persons[0].registeredAddress.streetCode|0010
c|persons[0].registeredAddress.streetNumber|19
c|persons[0].registeredAddress.streetType|ул
c|persons[0].registeredAddress.taxCode|152300
c|persons[0].registeredAddress.town|Тутаев
c|persons[0].registeredAddress.townCode|001
c|persons[0].registeredAddress.townType|г
c|persons[0].registeredAddress.zipCode|152306
c|persons[0].sex|m
n|salesPoint.addTerritories|1
n|salesPoint.approvalScanCopy|1
c|salesPoint.contractTypeSalesRoom|TA5
n|salesPoint.groupSellerplaceNumber|9
n|salesPoint.insuranceDeferred|0
n|salesPoint.multiProductSelection|0
n|salesPoint.photoDeferred|0
n|salesPoint.photoMandatory|1
n|salesPoint.remotePoint|0
n|salesPoint.salesArea|20
c|salesPoint.sellerCode|11717
n|salesPoint.sellerchainId|29394
c|salesPoint.sellerchainName|АО «Связной Логистика»,
c|salesPoint.sellerplaceAuthorizWay|Web Client
c|salesPoint.sellerplaceChain|АО «Связной Логистика»,
c|salesPoint.sellerplaceChainGroup|Связной
c|salesPoint.sellerplaceChainGroupCat|FED
c|salesPoint.sellerplaceCode|781471
d|salesPoint.sellerplaceDateContact|29.05.2009 00:00:00
d|salesPoint.sellerplaceDateCreate|31.03.2011 00:00:00
c|salesPoint.sellerplaceDirection|Центр
c|salesPoint.sellerplaceLocalityType|г
n|salesPoint.sellerplacePosOnCard|1
c|salesPoint.sellerplaceQualityRD|SMALL
c|salesPoint.sellerplaceQualitySC|SMALL
c|salesPoint.sellerplaceQualitySS|GOOD
c|salesPoint.sellerplaceRegCenter|Орловское
c|salesPoint.sellerplaceRegion|78
c|salesPoint.sellerplaceRegionCode|76
c|salesPoint.sellerplaceRegionName|Ярославская
c|salesPoint.sellerplaceSegment|Связь
c|salesPoint.sellerplaceStreet|Моторостроителей
c|salesPoint.sellerplaceStreetNumber|63б
c|salesPoint.sellerplaceTown|Тутаев
c|salesPoint.sellerplaceTownType|г
c|salesPoint.sellerplaceTypeAgree|ТТ без АП
c|salesPoint.sellerplaceZip|152306
n|salesPoint.smsMobileCheckAvailable|1
c|salesPoint.typeSalesroom|1
n|sourceData.hardCheckPredictors.correctDownpayment|0
n|sourceData.hardCheckPredictors.numContracts3months|0
n|sourceData.creditLimit.persons[0].cuid|60268391
n|sourceData.crossClientChecks.sameIdentCard.applicationCnt|1
n|sourceData.crossClientChecks.sameIdentCard.contactAddressApartmentCnt|1
n|sourceData.crossClientChecks.sameIdentCard.contactAddressStreetNumCnt|1
n|sourceData.crossClientChecks.sameIdentCard.employerName|1
n|sourceData.crossClientChecks.sameIdentCard.eqGoodsBrandCnt|0
n|sourceData.crossClientChecks.sameIdentCard.homePhoneCnt|1
n|sourceData.crossClientChecks.sameIdentCard.mobilePhoneCnt|1
n|sourceData.crossClientChecks.sameIdentCard.prodCodeCnt|1
n|sourceData.crossClientChecks.sameIdentCard.sellerplaceAddressStreetNumCnt|1
n|sourceData.crossClientChecks.sameIdentCard.sellerplaceCnt|1
n|sourceData.crossClientChecks.sameIdentCard.webMobilePhoneCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.applicationCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.cntIdentCardCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.contactAddressApartmentCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.diffContactAddressStreetNum|0
n|sourceData.crossClientChecks.sameMobileCheck.homePhoneCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.lastName3LettCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.sellerplaceCnt|0
n|sourceData.crossClientChecks.sameMobileCheck.webIdentCardCnt|0
n|sourceData.hardCheckPredictors.persons[0].MaxDPD4unpaidPenaltiesContracts|0
n|sourceData.hardCheckPredictors.persons[0].activeRu|0
n|sourceData.hardCheckPredictors.persons[0].actualDpdTolerance|0
n|sourceData.hardCheckPredictors.persons[0].annuityNextMonth|0
n|sourceData.hardCheckPredictors.persons[0].consolidatedPenalties|0
n|sourceData.hardCheckPredictors.persons[0].cuid|60268391
n|sourceData.hardCheckPredictors.persons[0].currentDebt|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtCar|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtCash|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtCashIC|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtIC|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtPos|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtPosIC|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtRevolving|0
n|sourceData.hardCheckPredictors.persons[0].currentDebtRevolvingIC|0
n|sourceData.hardCheckPredictors.persons[0].currentInsuranceDebt|0
n|sourceData.hardCheckPredictors.persons[0].currentInsuranceDebtIC|0
n|sourceData.hardCheckPredictors.persons[0].equalityDataAgreement|1
n|sourceData.hardCheckPredictors.persons[0].equalityDataAgreementSpecial|1
n|sourceData.hardCheckPredictors.persons[0].equalityEmpFrom|1
n|sourceData.hardCheckPredictors.persons[0].maxDpdTol6m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD_12m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD_24m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD_36m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD_48m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD_60m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolNotRD_6m|0
n|sourceData.hardCheckPredictors.persons[0].maxDpdTolerance|0
n|sourceData.hardCheckPredictors.persons[0].numGuarantedContracts|0
n|sourceData.hardCheckPredictors.persons[0].salaryChange1DTol|0
n|sourceData.hardCheckPredictors.persons[0].salaryChange7DTol|0
n|sourceData.hardCheckPredictors.persons[0].sumDebtRevolvingHomer|0
n|sourceData.hardCheckPredictors.persons[0].sumDebtRevolvingTW|0
n|sourceData.hardCheckPredictors.persons[0].sumDebtRevolvingTWInstalment|0
n|sourceData.hardCheckPredictors.persons[0].sumLimitRevolvingHomer|0
n|sourceData.hardCheckPredictors.persons[0].sumLimitRevolvingTW|0
n|sourceData.hardCheckPredictors.persons[0].totalDebt|0
n|sourceData.hardCheckPredictors.persons[0].totalSettled|0
n|sourceData.hardCheckPredictors.persons[0].undesirablePhones|1
n|bombInBank|0
n|calculateLinkedRDLimits|1
c|empCode|903570
c|employeeAdminType|s
c|evidSrv|2337158010
n|featureControl|1
n|idCredit|211986061
n|idPerson|51151942
n|idRequest|233180390
n|isOuterLimit|1
n|randomNumber1|0.15459536
n|randomNumber2|0.04144636
n|randomNumber3|0.41536653
n|randomNumber4|0.30515425
n|randomNumber5|0.30619656
n|randomNumber6|0.6669647
n|randomNumber7|0.02261733
n|randomNumber8|0.87043984
d|sysdate|14.05.2020 16:02:22
c|systemMessage|creditType=SS|SC|RD|MS|POSOL|SSMFO;vip_crType=SC|MS|SS|RD|POSOL|SSMFO;Portion=2;wfCode=-SCAN_CHECK_S;CAMP=GM3CUR100|PDNPLANB|YELLOWOFFERS|PRCUWRD0|PRCUWSC0|PRCUWPOS0;Portion2=2;wfCode2=-SCAN_CHECK_S;crType2=SS|SC|RD|POSOL|SSMFO;vip_parAmt=10000;vip_endDat=15.05.2020;vip_docNum=5004578753|4512861608;vip_SG=256;vip_amount=10000
n|timeZone|0
d|consent[0].consentDate|14.05.2020 00:00:00
d|consent[0].consentEndDate|14.11.2020 00:00:00
n|consent[0].consentFlag|1
c|consent[0].consentOwner|HCFB
c|consent[0].consentSubjectType|BKI
d|consent[1].consentDate|14.05.2020 00:00:00
n|consent[1].consentFlag|1
c|consent[1].consentOwner|HCFB
c|consent[1].consentSubjectType|BEELINE;MTS;TELE2;MEGAFON;MAILRU;FACETZ;PERSONAL_DATA;YANDEX
c|persons[0].mobileOperator|ПАО "Мобильные ТелеСистемы"
c|salesPoint.products[0].productFamily|PF_CC_TW_2L
c|salesPoint.products[0].productFamilyType|RD
c|salesPoint.products[1].productFamily|PF_CL_STND
c|salesPoint.products[1].productFamilyType|SC
c|salesPoint.products[2].productFamily|PF_CC_HOMER_POLZA
c|salesPoint.products[2].productFamilyType|RD
c|salesPoint.products[3].productFamily|PF_CC_HOMER_CASHONCARD
c|salesPoint.products[3].productFamilyType|RD
c|salesPoint.products[4].productFamily|PF_CC_HOMER_CASHVIACARD
c|salesPoint.products[4].productFamilyType|RD
n|sourceData.biometricData.persons[0].cuid|60268391
n|sourceData.biometricData.persons[0].photoId|93059199
n|workflow.stageCounters[0].WFSTAGE_INDEX|7402
n|workflow.stageCounters[1].WFSTAGE_INDEX|6095
n|workflow.stageCounters[2].WFSTAGE_INDEX|3286
n|workflow.stageCounters[3].WFSTAGE_INDEX|7497
n|workflow.stageCounters[4].WFSTAGE_INDEX|7121
n|workflow.stageCounters[5].WFSTAGE_INDEX|2761
n|workflow.stageCounters[6].WFSTAGE_INDEX|2762
n|workflow.stageCounters[7].WFSTAGE_INDEX|8410
c|calculateOnlineLimit|0
c|credit.parentId|211986061
n|outputData.checkPersons[0].cuid|60268391
c|outputData.checkPersons[0].workflowCode|FPS_AFS
n|outputData.resultTrace[0].cuid|60268391
c|outputData.resultTrace[0].resultName|prelimResult
c|persons[0].snilsCheck|DOC_NFOUND
c|prelimResult.finalRiskGroup|1
c|prelimResult.nextStrategy|FPS
c|prelimResult.riskGroup|1
c|prelimResult.strategyName|POS New
c|prelimResult.strategyPassLog|UNEMPLOYED;SELLER;AP;SPLITCALL;CL_PRICE_CHAMPION;ACQ_XGB_4_201907;SOFT_MODERATE;CL_REFIN_MINPRICE
c|prelimResult.strategyType|Champion
c|prelimResult.strategyVersion|01.05.2016
c|prelimResult.strategyVersionDate|4/17/20 1:39 PM
c|prelimResult.workflowCode|FPS_AFS
n|prelimResult.client.availableForSale|0
c|prelimResult.client.processLine|SPLITCALL;CL_PRICE_CHAMPION;SOFT_MODERATE;CL_REFIN_MINPRICE
n|prelimResult.derivedData.persons[0].cuid|60268391
n|prelimResult.derivedData.persons[0].undesirablePeriod|0
n|prelimResult.persons[0].cuid|60268391
n|prelimResult.score.persons[0].cuid|60268391
n|workflow.stageCounters[8].WFSTAGE_INDEX|6816
n|workflow.stageCounters[9].WFSTAGE_INDEX|6815
n|workflow.stageCounters[10].WFSTAGE_INDEX|2764
n|workflow.stageCounters[11].WFSTAGE_INDEX|2765
n|workflow.stageCounters[12].WFSTAGE_INDEX|2768
n|workflow.stageCounters[13].WFSTAGE_INDEX|8011
n|workflow.stageCounters[14].WFSTAGE_INDEX|13585
n|workflow.stageCounters[15].WFSTAGE_INDEX|7117
n|workflow.stageCounters[16].WFSTAGE_INDEX|6946
n|workflow.stageCounters[17].WFSTAGE_INDEX|6949
n|workflow.stageCounters[18].WFSTAGE_INDEX|6947
n|workflow.stageCounters[19].WFSTAGE_INDEX|6948
n|workflow.stageCounters[20].WFSTAGE_INDEX|6950
n|workflow.stageCounters[21].WFSTAGE_INDEX|9067
n|workflow.stageCounters[22].WFSTAGE_INDEX|6804
n|workflow.stageCounters[23].WFSTAGE_INDEX|6808
c|credit.afs.mainRules|38_2=1;106_2=5;
n|credit.creditBureau.bureauResponse[0].cache_use|0
c|credit.creditBureau.bureauResponse[0].cbId|AFS
n|credit.creditBureau.bureauResponse[0].code|0
c|credit.fps.responseStatusFlag|0
n|workflow.stageCounters[24].WFSTAGE_INDEX|6807
n|workflow.stageCounters[25].WFSTAGE_INDEX|6809
n|workflow.stageCounters[26].WFSTAGE_INDEX|6810
n|workflow.stageCounters[27].WFSTAGE_INDEX|6811
n|workflow.stageCounters[25].WFSTAGE_INDEX|1
c|credit.fps.mainRules|1.11=>0;1.12=>0;1.13=>0;1.14=>0;1.15=>0;1.16=>0;1.17=>0;1.18=>0;1.19=>0;1.20=>0;1.21=>0;1.41=>0;1.42=>0;2.11=>0;2.12=>0;2.13=>0;2.14=>0;2.15=>0;2.16=>0;2.17=>0;2.18=>0;2.19=>0;2.20=>0;2.21=>0;2.22=>0;2.23=>0;2.24=>1;2.25=>0;2.26=>1;2.27=>1;2.28=>0;2.29=>0;2.30=>0;2.31=>0;2.32=>0;2.33=>0;2.34=>0;2.35=>0;2.36=>0;2.37=>0;2.38=>0;2.41=>0.3167;2.42=>0.3566;2.44=>0.4289;5.1=>0;5.2=>0;5.3=>0;5.4=>0;6.1=>0;6.2=>0;7.1=>0;7.2=>0;7.3=>0;7.4=>0;7.5=>0;7.6=>0;7.7=>0;7.8=>0;7.9=>0;7.10=>0;7.11=>0;7.12=>0;7.13=>0;7.14=>0;7.15=>0;7.16=>0;7.17=>1;7.18=>0;7.19=>1;7.20=>1;7.87=>0;7.88=>0;7.97=>0;7.98=>0;7.99=>1;7.100=>0;7.101=>0;
n|credit.fps.mainScoreValue|213
n|credit.fps.numApplicationsFound|40
c|credit.fps.responseStatusVector|0
c|credit.fps.specificRules|1.901=>1;1.2001=>0;1.2002=>0;2.901=>2;2.902=>0;2.903=>0;2.904=>1;2.905=>0;2.906=>1;2.907=>1;2.908=>0;2.909=>0;2.910=>0;2.911=>0;2.912=>3;2.913=>0;2.914=>0;2.915=>0;2.916=>0;2.917=>0;2.918=>1;2.919=>0;2.920=>0;2.921=>1;2.922=>2;2.923=>0;2.924=>2;2.925=>1;2.926=>0;2.927=>0;2.928=>1;2.929=>1;2.930=>0;2.931=>0;2.932=>0;2.933=>0;2.934=>0;2.935=>0;2.936=>0;2.937=>4;2.938=>5;2.939=>1;2.940=>0;2.941=>0;2.942=>0;2.943=>1;2.944=>1;2.945=>0;2.946=>0;2.947=>0;2.948=>0;2.949=>0;2.950=>0;2.951=>0;2.952=>0;2.953=>0;2.954=>0;2.1001=>0;2.1002=>0;2.1003=>0;2.1004=>0;2.1005=>0;2.1006=>0;2.1007=>0;2.1008=>-1;2.1009=>0;2.1010=>0;2.2001=>0;2.2002=>0;2.2003=>0;2.2004=>0;2.3001=>0;2.3002=>0;3.901=>0;3.902=>0;3.903=>1;4.1001=>0;7.95=>0;7.961=>0.952;7.1001=>1;7.1011=>-1;8.901=>0;8.902=>0;
c|fpsResult.finalRiskGroup|1
c|fpsResult.nextStrategy|Credit-Bureau
c|fpsResult.riskGroup|1
c|fpsResult.strategyName|POS New
c|fpsResult.strategyPassLog|UNEMPLOYED;SELLER;AP;SPLITCALL;CL_PRICE_CHAMPION;ACQ_XGB_4_201907;SOFT_MODERATE
c|fpsResult.strategyType|Champion
c|fpsResult.strategyVersion|01.05.2016
c|fpsResult.strategyVersionDate|5/12/20 3:51 PM
c|fpsResult.workflowCode|CREDIT_REGISTRY
n|fpsResult.client.availableForSale|0
c|fpsResult.client.processLine|SPLITCALL;CL_PRICE_CHAMPION;SOFT_MODERATE
n|fpsResult.derivedData.persons[0].cuid|60268391
n|fpsResult.derivedData.persons[0].undesirablePeriod|0
c|fpsResult.persons[0].bkiList|equ,nbk,exp
c|fpsResult.persons[0].bkiSource|BANK
c|fpsResult.persons[0].bkiSubRequestCode|exp=111;equ=101
n|fpsResult.persons[0].cuid|60268391
c|fpsResult.score.score21Function|Greedy_XGB_201904
c|fpsResult.score.score22Function|Bureau_XGB_4_201910
c|fpsResult.score.score9Function|ACQ_XGB_4_201907
n|fpsResult.score.persons[0].cuid|60268391
n|fpsResult.score.persons[0].cutoffID|0
n|fpsResult.score.persons[0].cutoffValue|0
c|fpsResult.score.persons[0].scoreFunction|ACQ_XGB_4_201907
n|outputData.checkPersons[1].cuid|60268391
c|outputData.checkPersons[1].workflowCode|CREDIT_REGISTRY
n|outputData.resultTrace[1].cuid|60268391
c|outputData.resultTrace[1].resultName|fpsResult
n|workflow.stageCounters[28].WFSTAGE_INDEX|6812
n|workflow.stageCounters[29].WFSTAGE_INDEX|3249
n|workflow.stageCounters[30].WFSTAGE_INDEX|3248
n|workflow.stageCounters[31].WFSTAGE_INDEX|3258
n|workflow.stageCounters[32].WFSTAGE_INDEX|3257
n|workflow.stageCounters[33].WFSTAGE_INDEX|3256
n|workflow.stageCounters[34].WFSTAGE_INDEX|8009
n|workflow.stageCounters[35].WFSTAGE_INDEX|16025
n|workflow.stageCounters[36].WFSTAGE_INDEX|13581
n|workflow.stageCounters[37].WFSTAGE_INDEX|3254
n|workflow.stageCounters[38].WFSTAGE_INDEX|6598
n|credit.creditBureau.bureauResponse[1].cache_use|0
c|credit.creditBureau.bureauResponse[1].cbId|nbk
n|credit.creditBureau.bureauResponse[1].code|1
n|credit.creditBureau.bureauResponse[2].cache_use|0
c|credit.creditBureau.bureauResponse[2].cbId|equ
n|credit.creditBureau.bureauResponse[2].code|1
n|credit.creditBureau.bureauResponse[3].cache_use|0
c|credit.creditBureau.bureauResponse[3].cbId|exp
n|credit.creditBureau.bureauResponse[3].code|1
n|workflow.stageCounters[31].WFSTAGE_INDEX|1
n|workflow.stageCounters[32].WFSTAGE_INDEX|1
n|workflow.stageCounters[39].WFSTAGE_INDEX|6597
n|workflow.stageCounters[40].WFSTAGE_INDEX|6596
n|workflow.stageCounters[41].WFSTAGE_INDEX|3245
n|workflow.stageCounters[42].WFSTAGE_INDEX|3244
n|workflow.stageCounters[33].WFSTAGE_INDEX|1
c|cbResult.finalRiskGroup|1
c|cbResult.nextStrategy|Big-Data_B
c|cbResult.riskGroup|1
c|cbResult.strategyName|POS New
c|cbResult.strategyPassLog|UNEMPLOYED;SELLER;AP;HIGH_PTI;SPLITCALL;CL_PRICE_CHAMPION;ACQ_XGB_4_201907;SOFT_MODERATE
c|cbResult.strategyType|Champion
c|cbResult.strategyVersion|01.05.2016
c|cbResult.strategyVersionDate|5/12/20 3:53 PM
c|cbResult.workflowCode|CREDIT_REGISTRY;SMART_DATA;BIG_DATA
n|cbResult.client.availableForSale|0
c|cbResult.client.processLine|SPLITCALL;CL_PRICE_CHAMPION;SOFT_MODERATE
n|cbResult.derivedData.persons[0].cuid|60268391
n|cbResult.derivedData.persons[0].undesirablePeriod|0
c|cbResult.persons[0].bigDataList|MAILRUSCORE;MEGAFON;MTSMULTISCORE;BEE;EQMULTISCORE
c|cbResult.persons[0].bkiList|equ,nbk,exp
c|cbResult.persons[0].bkiSource|BANK
c|cbResult.persons[0].bkiSubRequestCode|exp=113;exp=111;equ=101;equ=102
n|cbResult.persons[0].cuid|60268391
c|cbResult.request[0].reqCampaign|EQMULTISCORE
c|cbResult.request[0].reqCode|type
c|cbResult.request[0].reqType|string
c|cbResult.request[0].reqValue|1234575404
c|cbResult.request[1].reqCampaign|BEE
c|cbResult.request[1].reqCode|ModelName
c|cbResult.request[1].reqType|string
c|cbResult.request[1].reqValue|UNI_POS_V2
c|cbResult.request[2].reqCampaign|MAILRUSCORE
c|cbResult.request[2].reqCode|ModelName
c|cbResult.request[2].reqType|string
c|cbResult.request[2].reqValue|hmc_mailru_201906
c|cbResult.request[3].reqCampaign|MEGAFON
c|cbResult.request[3].reqCode|variables
c|cbResult.request[3].reqType|string
c|cbResult.request[3].reqValue|MEG_HCFB_6_60_201906
c|cbResult.request[4].reqCampaign|MTSMULTISCORE
c|cbResult.request[4].reqCode|features
c|cbResult.request[4].reqType|string
c|cbResult.request[4].reqValue|HCFB_MTS_CL_201808;HCFB_MTS_COMP_201711
c|cbResult.request[5].reqCampaign|MTSMULTISCORE
c|cbResult.request[5].reqCode|DOC_SEND_FLAG
c|cbResult.request[5].reqType|string
c|cbResult.request[5].reqValue|0
c|cbResult.request[6].reqCampaign|MTSMULTISCORE
c|cbResult.request[6].reqCode|FIO_SEND_FLAG
c|cbResult.request[6].reqType|string
c|cbResult.request[6].reqValue|0
c|cbResult.request[7].reqCampaign|MTSMULTISCORE
c|cbResult.request[7].reqCode|DR_SEND_FLAG
c|cbResult.request[7].reqType|string
c|cbResult.request[7].reqValue|1
c|cbResult.score.score21Function|Greedy_XGB_201904
c|cbResult.score.score22Function|Bureau_XGB_4_201910
c|cbResult.score.score9Function|ACQ_XGB_4_201907
n|cbResult.score.persons[0].cuid|60268391
n|cbResult.score.persons[0].cutoffID|0
n|cbResult.score.persons[0].cutoffValue|0
c|cbResult.score.persons[0].scoreFunction|ACQ_XGB_4_201907
c|cbResult.sdQuery[0].attributes|address_type_mts_geo,act_type_mts_geo,quarter_mts_geo,percent_mts_geo,act_date_calculation_mts_geo
c|cbResult.sdQuery[0].context_ii|ii_mts_geo_activity
c|cbResult.sdQuery[0].entity|geo_activity
c|cbResult.sdQuery[0].filter|evid_srv_mts_geo==2337158010,act_date_calculation_mts_geo > 2020-05-07 00:00:00,address_type_mts_geo==1
c|cbResult.sdQuery[0].mode|upsert
n|cbResult.sdQuery[0].reqGroupId|1
c|cbResult.sdQuery[0].rowkey|null
n|cbResult.sdQuery[0].stale|43200
n|cbResult.sdQuery[0].timeoutBP|1
n|cbResult.sdQuery[0].timeoutSD|9
c|cbResult.sdQuery[1].attributes|score_value_mailru,score_date_calculation_mailru,score_method_name_mailru,score_model_code_mailru
c|cbResult.sdQuery[1].context_ii|ii_mailru_geoscore
c|cbResult.sdQuery[1].entity|client_score
c|cbResult.sdQuery[1].mode|upsert
n|cbResult.sdQuery[1].reqGroupId|1
c|cbResult.sdQuery[1].rowkey|hmc_reg_geo
n|cbResult.sdQuery[1].stale|43200
n|cbResult.sdQuery[1].timeoutBP|1
n|cbResult.sdQuery[1].timeoutSD|9
c|cbResult.sdQuery[2].attributes|days_servlen_current_calendar_year_pfr_account_advice,infdate_pfr_account_advice,average_monthly_income_last_12_months_pfr_account_advice,penssumval_pfr_account_advice
c|cbResult.sdQuery[2].context_ii|ii_pfr_account_advice
c|cbResult.sdQuery[2].entity|smuid_data
c|cbResult.sdQuery[2].mode|none
n|cbResult.sdQuery[2].reqGroupId|2
n|cbResult.sdQuery[2].stale|43200
n|cbResult.sdQuery[2].timeoutBP|0
n|cbResult.sdQuery[2].timeoutSD|10
c|cbResult.sdQueryContext[0].params|BlazeAddressType=1;stale_context=2020-05-07 00:00:00
c|cbResult.sdQueryContext[0].topic|ii_mts_geo_activity
c|cbResult.sdQueryContext[1].topic|ii_mailru_geoscore
c|cbResult.sdQueryContext[2].topic|ii_pfr_account_advice
n|outputData.checkPersons[2].cuid|60268391
c|outputData.checkPersons[2].workflowCode|CREDIT_REGISTRY;SMART_DATA;BIG_DATA
n|outputData.resultTrace[2].cuid|60268391
c|outputData.resultTrace[2].resultName|cbResult
n|workflow.stageCounters[34].WFSTAGE_INDEX|1
n|workflow.stageCounters[35].WFSTAGE_INDEX|1
n|workflow.stageCounters[36].WFSTAGE_INDEX|1
n|workflow.stageCounters[37].WFSTAGE_INDEX|1
n|workflow.stageCounters[38].WFSTAGE_INDEX|1
n|credit.creditBureau.bureauResponse[4].cache_use|1
c|credit.creditBureau.bureauResponse[4].cbId|nbk
n|credit.creditBureau.bureauResponse[4].code|1
n|credit.creditBureau.bureauResponse[5].cache_use|1
c|credit.creditBureau.bureauResponse[5].cbId|equ
n|credit.creditBureau.bureauResponse[5].code|1
n|credit.creditBureau.bureauResponse[6].cache_use|0
c|credit.creditBureau.bureauResponse[6].cbId|equ
n|credit.creditBureau.bureauResponse[6].code|25
n|credit.creditBureau.bureauResponse[7].cache_use|0
c|credit.creditBureau.bureauResponse[7].cbId|exp
n|credit.creditBureau.bureauResponse[7].code|1
n|credit.creditBureau.bureauResponse[8].cache_use|1
c|credit.creditBureau.bureauResponse[8].cbId|exp
n|credit.creditBureau.bureauResponse[8].code|1
c|credit.creditBureau.persons[0].bkiListQuery|equ,nbk,exp
n|credit.creditBureau.persons[0].cuid|60268391
d|credit.creditBureau.persons[0].queryDate|14.05.2020 16:02:38
c|credit.creditBureau.persons[0].querySource|BANK
c|credit.creditBureau.persons[0].addresses.address[0].act_type|act
c|credit.creditBureau.persons[0].addresses.address[0].address_type|reg
c|credit.creditBureau.persons[0].addresses.address[0].full_address|ТУТАЕВСКИЙ, Г ТУТАЕВ ТУТАЕВ, 152300 ОБЛ ЯРОСЛАВСКАЯ Г ТУТАЕВ Р-Н ТУТАЕВСКИЙ УЛ ДЕМЕНТЬЕВА ДОМ 19 КВ 180, , ДЕМЕНТЬЕВА Д 19, 19, , , 180
c|credit.creditBureau.persons[0].addresses.address[1].act_type|act
c|credit.creditBureau.persons[0].addresses.address[1].address_type|fact
c|credit.creditBureau.persons[0].addresses.address[1].full_address|, Г ТУТАЕВ ТУТАЕВ, 152300 ОБЛ ЯРОСЛАВСКАЯ Г ТУТАЕВ Р-Н ТУТАЕВСКИЙ УЛ ДЕМЕНТЬЕВА ДОМ 19 КВ 180, , ДЕМЕНТЬЕВА Д 19, 19, , , 180
c|credit.creditBureau.persons[0].addresses.address[2].act_type|his
d|credit.creditBureau.persons[0].addresses.address[2].actuality_date|18.11.2015 00:00:00
c|credit.creditBureau.persons[0].addresses.address[2].address_type|fact
c|credit.creditBureau.persons[0].addresses.address[2].full_address|152325, ОБЛ ЯРОСЛАВСКАЯ, Р-Н ТУТАЕВСКИЙ, Д СТОЛБИЩИ, УЛ МОЛОДЕЖНАЯ, ДОМ 3, КВ 1
c|credit.creditBureau.persons[0].requests.request[0].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[0].cred_sum|18817
n|credit.creditBureau.persons[0].requests.request[0].cred_type|99
n|credit.creditBureau.persons[0].requests.request[0].partner_type|1
n|credit.creditBureau.persons[0].requests.request[0].timeslot|3
c|credit.creditBureau.persons[0].requests.request[1].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[1].cred_sum|0
n|credit.creditBureau.persons[0].requests.request[1].cred_type|99
n|credit.creditBureau.persons[0].requests.request[1].partner_type|1
n|credit.creditBureau.persons[0].requests.request[1].timeslot|4
c|credit.creditBureau.persons[0].requests.request[2].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[2].cred_sum|15000
n|credit.creditBureau.persons[0].requests.request[2].cred_type|5
n|credit.creditBureau.persons[0].requests.request[2].partner_type|1
n|credit.creditBureau.persons[0].requests.request[2].timeslot|5
c|credit.creditBureau.persons[0].requests.request[3].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[3].cred_sum|300000
n|credit.creditBureau.persons[0].requests.request[3].cred_type|5
n|credit.creditBureau.persons[0].requests.request[3].partner_type|1
n|credit.creditBureau.persons[0].requests.request[3].timeslot|5
c|credit.creditBureau.persons[0].requests.request[4].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[4].cred_sum|15000
n|credit.creditBureau.persons[0].requests.request[4].cred_type|5
n|credit.creditBureau.persons[0].requests.request[4].partner_type|1
n|credit.creditBureau.persons[0].requests.request[4].timeslot|6
n|credit.creditBureau.persons[0].requests.request[5].partner_type|1
n|credit.creditBureau.persons[0].requests.request[5].timeslot|5
c|credit.creditBureau.persons[0].requests.request[6].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[6].cred_sum|0
n|credit.creditBureau.persons[0].requests.request[6].cred_type|99
n|credit.creditBureau.persons[0].requests.request[6].partner_type|1
n|credit.creditBureau.persons[0].requests.request[6].timeslot|3
c|credit.creditBureau.persons[0].requests.request[7].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[7].cred_sum|17921
n|credit.creditBureau.persons[0].requests.request[7].cred_type|99
n|credit.creditBureau.persons[0].requests.request[7].partner_type|1
n|credit.creditBureau.persons[0].requests.request[7].timeslot|3
c|credit.creditBureau.persons[0].requests.request[8].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[8].cred_sum|0
n|credit.creditBureau.persons[0].requests.request[8].cred_type|99
n|credit.creditBureau.persons[0].requests.request[8].partner_type|1
n|credit.creditBureau.persons[0].requests.request[8].timeslot|4
c|credit.creditBureau.persons[0].requests.request[9].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[9].cred_sum|15000
n|credit.creditBureau.persons[0].requests.request[9].cred_type|5
n|credit.creditBureau.persons[0].requests.request[9].partner_type|1
n|credit.creditBureau.persons[0].requests.request[9].timeslot|4
c|credit.creditBureau.persons[0].requests.request[10].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[10].cred_sum|300000
n|credit.creditBureau.persons[0].requests.request[10].cred_type|99
n|credit.creditBureau.persons[0].requests.request[10].partner_type|1
n|credit.creditBureau.persons[0].requests.request[10].timeslot|4
c|credit.creditBureau.persons[0].requests.request[11].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[11].cred_sum|270000
n|credit.creditBureau.persons[0].requests.request[11].cred_type|99
n|credit.creditBureau.persons[0].requests.request[11].partner_type|1
n|credit.creditBureau.persons[0].requests.request[11].timeslot|5
c|credit.creditBureau.persons[0].requests.request[12].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[12].cred_sum|270000
n|credit.creditBureau.persons[0].requests.request[12].cred_type|99
n|credit.creditBureau.persons[0].requests.request[12].partner_type|1
n|credit.creditBureau.persons[0].requests.request[12].timeslot|6
c|credit.creditBureau.persons[0].requests.request[13].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[13].cred_sum|270000
n|credit.creditBureau.persons[0].requests.request[13].cred_type|99
n|credit.creditBureau.persons[0].requests.request[13].partner_type|1
n|credit.creditBureau.persons[0].requests.request[13].timeslot|6
c|credit.creditBureau.persons[0].requests.request[14].cred_currency|rur
n|credit.creditBureau.persons[0].requests.request[14].cred_sum|0
n|credit.creditBureau.persons[0].requests.request[14].cred_type|99
n|credit.creditBureau.persons[0].requests.request[14].partner_type|1
n|credit.creditBureau.persons[0].requests.request[14].timeslot|6
n|workflow.stageCounters[39].WFSTAGE_INDEX|1
c|credit.creditBureau.scoring[0].cbId|equ
n|credit.creditBureau.scoring[0].cuid|60268391
n|credit.creditBureau.scoring[0].score|687
n|credit.creditBureau.scoring[0].scoreCardID|23
c|credit.creditBureau.scoring[1].cbId|exp
n|credit.creditBureau.scoring[1].cuid|60268391
n|credit.creditBureau.scoring[1].score|978
n|credit.creditBureau.scoring[1].scoreCardID|113
c|sourceData.nextWorkflows[0].workflowCode|SMART_DATA;BIG_DATA
n|workflow.stageCounters[31].WFSTAGE_INDEX|1
n|workflow.stageCounters[37].WFSTAGE_INDEX|1
n|workflow.stageCounters[40].WFSTAGE_INDEX|1
n|workflow.stageCounters[41].WFSTAGE_INDEX|1
n|workflow.stageCounters[42].WFSTAGE_INDEX|1
n|workflow.stageCounters[43].WFSTAGE_INDEX|7394
n|workflow.stageCounters[44].WFSTAGE_INDEX|7395
n|workflow.stageCounters[45].WFSTAGE_INDEX|7396
n|workflow.stageCounters[46].WFSTAGE_INDEX|7397
c|sourceData.nextWorkflows[1].workflowCode|BIG_DATA
n|workflow.stageCounters[31].WFSTAGE_INDEX|1
n|workflow.stageCounters[37].WFSTAGE_INDEX|1
n|workflow.stageCounters[44].WFSTAGE_INDEX|1
n|workflow.stageCounters[47].WFSTAGE_INDEX|7398
n|workflow.stageCounters[48].WFSTAGE_INDEX|3234
n|workflow.stageCounters[49].WFSTAGE_INDEX|3235
n|workflow.stageCounters[50].WFSTAGE_INDEX|3236
c|agregatorResult[0].agregatorCode|BEE
c|agregatorResult[0].agregatorParamCode|Score
c|agregatorResult[0].agregatorParamType|CHAR_VALUE
c|agregatorResult[0].agregatorParamValue|1.032481375460823
c|agregatorResult[0].agregatorSegment|BEE
c|agregatorResult[1].agregatorCode|BEE
c|agregatorResult[1].agregatorParamCode|ModelName
c|agregatorResult[1].agregatorParamType|CHAR_VALUE
c|agregatorResult[1].agregatorParamValue|UNI_POS_V2
c|agregatorResult[1].agregatorSegment|BEE
c|agregatorResult[2].agregatorCode|MAILRUSCORE
c|agregatorResult[2].agregatorParamCode|Score
c|agregatorResult[2].agregatorParamType|NUM_VALUE
c|agregatorResult[2].agregatorParamValue|0.6006865587
c|agregatorResult[2].agregatorSegment|MAILRUSCORE
c|agregatorResult[3].agregatorCode|MAILRUSCORE
c|agregatorResult[3].agregatorParamCode|ScoreGetDateTime
c|agregatorResult[3].agregatorParamType|DTIME_VALUE
c|agregatorResult[3].agregatorParamValue|2020-05-14T00:00:00
c|agregatorResult[3].agregatorSegment|MAILRUSCORE
c|agregatorResult[4].agregatorCode|MAILRUSCORE
c|agregatorResult[4].agregatorParamCode|MatchingLevel
c|agregatorResult[4].agregatorParamType|NUM_VALUE
c|agregatorResult[4].agregatorParamValue|5
c|agregatorResult[4].agregatorSegment|MAILRUSCORE
c|agregatorResult[5].agregatorCode|MAILRUSCORE
c|agregatorResult[5].agregatorParamCode|ModelName
c|agregatorResult[5].agregatorParamType|CHAR_VALUE
c|agregatorResult[5].agregatorParamValue|hmc_mailru_201906
c|agregatorResult[5].agregatorSegment|MAILRUSCORE
c|agregatorResult[6].agregatorCode|MAILRUSCORE
c|agregatorResult[6].agregatorParamCode|Method
c|agregatorResult[6].agregatorParamType|CHAR_VALUE
c|agregatorResult[6].agregatorParamValue|GetStreetClientScore
c|agregatorResult[6].agregatorSegment|MAILRUSCORE
c|agregatorResult[7].agregatorCode|MEGAFON
c|agregatorResult[7].agregatorParamCode|MEG_HCFB_6_60_201906
c|agregatorResult[7].agregatorParamType|CHAR_VALUE
c|agregatorResult[7].agregatorParamValue|0.078778259;SUCCESS
c|agregatorResult[7].agregatorSegment|MFSCORE
c|agregatorResult[8].agregatorCode|MTSMULTISCORE
c|agregatorResult[8].agregatorParamCode|alien
c|agregatorResult[8].agregatorParamType|CHAR_VALUE
c|agregatorResult[8].agregatorParamValue|false
c|agregatorResult[8].agregatorSegment|MTSMULTISCORE
c|agregatorResult[9].agregatorCode|MTSMULTISCORE
c|agregatorResult[9].agregatorParamCode|HCFB_MTS_CL_201808
c|agregatorResult[9].agregatorParamType|NUM_VALUE
c|agregatorResult[9].agregatorParamValue|0.05411228
c|agregatorResult[9].agregatorSegment|MTSMULTISCORE
c|agregatorResult[10].agregatorCode|MTSMULTISCORE
c|agregatorResult[10].agregatorParamCode|HCFB_MTS_COMP_201711
c|agregatorResult[10].agregatorParamType|CHAR_VALUE
c|agregatorResult[10].agregatorParamValue|ERR:There is no data available for feature [HCFB_MTS_COMP_201711]
c|agregatorResult[10].agregatorSegment|MTSMULTISCORE
c|agregatorResult[11].agregatorCode|MTSMULTISCORE
c|agregatorResult[11].agregatorParamCode|CacheUse
c|agregatorResult[11].agregatorParamType|CHAR_VALUE
c|agregatorResult[11].agregatorParamValue|HCFB_MTS_CL_201808:0;HCFB_MTS_COMP_201711:0;
c|agregatorResult[11].agregatorSegment|MTSMULTISCORE
c|agregatorResult[12].agregatorCode|EQMULTISCORE
c|agregatorResult[12].agregatorParamCode|1234575404
c|agregatorResult[12].agregatorParamType|NUM_VALUE
c|agregatorResult[12].agregatorParamValue|633
c|agregatorResult[12].agregatorSegment|EQMULTISCORE
c|agregatorResult[13].agregatorCode|EQMULTISCORE
c|agregatorResult[13].agregatorParamCode|CacheUse
c|agregatorResult[13].agregatorParamType|CHAR_VALUE
c|agregatorResult[13].agregatorParamValue|1234575404:0;
c|agregatorResult[13].agregatorSegment|EQMULTISCORE
c|smData.client_score.mailru_score[0].score_date_calculation_mailru|2020-05-14 16:02:47
c|smData.client_score.mailru_score[0].score_method_name_mailru|GetStreetClientScore
c|smData.client_score.mailru_score[0].score_model_code_mailru|hmc_reg_geo
n|smData.client_score.mailru_score[0].score_value_mailru|0.7913591869
c|smData.geo_activity.mts_geo_activity[0].act_date_calculation_mts_geo|2020-05-14 16:02:48.713
c|smData.geo_activity.mts_geo_activity[0].act_type_mts_geo|voice
n|smData.geo_activity.mts_geo_activity[0].address_type_mts_geo|1
c|smData.geo_activity.mts_geo_activity[0].evid_srv_mts_geo|2337158010
n|smData.geo_activity.mts_geo_activity[0].percent_mts_geo|20
c|smData.geo_activity.mts_geo_activity[0].quarter_mts_geo|2
c|smData.geo_activity.mts_geo_activity[1].act_date_calculation_mts_geo|2020-05-14 16:02:48.713
c|smData.geo_activity.mts_geo_activity[1].act_type_mts_geo|voice
n|smData.geo_activity.mts_geo_activity[1].address_type_mts_geo|1
c|smData.geo_activity.mts_geo_activity[1].evid_srv_mts_geo|2337158010
n|smData.geo_activity.mts_geo_activity[1].percent_mts_geo|11
c|smData.geo_activity.mts_geo_activity[1].quarter_mts_geo|3
n|workflow.stageCounters[31].WFSTAGE_INDEX|1
n|workflow.stageCounters[32].WFSTAGE_INDEX|1
n|workflow.stageCounters[33].WFSTAGE_INDEX|1
n|workflow.stageCounters[51].WFSTAGE_INDEX|3237
n|workflow.stageCounters[52].WFSTAGE_INDEX|3238
n|workflow.stageCounters[53].WFSTAGE_INDEX|3239
n|workflow.stageCounters[54].WFSTAGE_INDEX|3240
c|bdResult.finalRiskGroup|1
c|bdResult.nextStrategy|POS-Score_B
c|bdResult.riskGroup|1
c|bdResult.strategyName|POS New
c|bdResult.strategyPassLog|UNEMPLOYED;SELLER;AP;HIGH_PTI;SPLITCALL;CL_PRICE_CHAMPION;SMDATA_MAILGEO_REG;SMDATA_MTSGEO_REG;ACQ_XGB_4_201907;SOFT_MODERATE;HITMEGAFON;HITMAILRU;HITMTS;HITBEELINE;HITFPS;HITEQUIFAX;HITBUREAU;HITSOCIALCIRCLE
c|bdResult.strategyType|Champion
c|bdResult.strategyVersion|01.05.2016
c|bdResult.strategyVersionDate|4/28/20 10:48 AM
c|bdResult.workflowCode|NAP_RESULT
n|bdResult.client.availableForSale|0
c|bdResult.client.processLine|SPLITCALL;CL_PRICE_CHAMPION;SOFT_MODERATE
n|bdResult.derivedData.persons[0].cuid|60268391
n|bdResult.derivedData.persons[0].undesirablePeriod|0
n|bdResult.persons[0].cuid|60268391
c|bdResult.score.score21Function|Greedy_XGB_201904
c|bdResult.score.score22Function|Bureau_XGB_4_201910
c|bdResult.score.score9Function|ACQ_XGB_4_201907
n|bdResult.score.persons[0].cuid|60268391
c|bdResult.score.persons[0].lineID|APPROVE
c|bdResult.score.persons[0].scoreFunction|ACQ_XGB_4_201907
n|outputData.checkPersons[3].cuid|60268391
c|outputData.checkPersons[3].workflowCode|NAP_RESULT
n|outputData.resultTrace[3].cuid|60268391
c|outputData.resultTrace[3].resultName|bdResult
c|sourceData.verificationDetailResults[0].activityCode|move_to_inline_wf
n|sourceData.verificationDetailResults[0].cuid|60268391
c|sourceData.verificationDetailResults[0].informationCode|NEXT_WFS
c|sourceData.verificationDetailResults[0].informationValue|9067
c|sourceData.verificationResults[0].activityCode|wflow.cif.identify.isDataChanged
c|sourceData.verificationResults[0].activityResult|AC_NEW
n|sourceData.verificationResults[0].cuid|60268391
c|sourceData.verificationResults[1].activityCode|wflow.cif.identify.short
c|sourceData.verificationResults[1].activityResult|NOT_FOUND
n|sourceData.verificationResults[1].cuid|60268391
c|sourceData.verificationResults[2].activityCode|storeWPS_Data
c|sourceData.verificationResults[2].activityResult|BD_CNFDB
n|sourceData.verificationResults[2].cuid|60268391
c|sourceData.verificationResults[3].activityCode|check_originator
c|sourceData.verificationResults[3].activityResult|NO
n|sourceData.verificationResults[3].cuid|60268391
c|sourceData.verificationResults[4].activityCode|snils.check
c|sourceData.verificationResults[4].activityResult|DOC_NFOUND
n|sourceData.verificationResults[4].cuid|60268391
c|sourceData.verificationResults[5].activityCode|blaze.prescoring
c|sourceData.verificationResults[5].activityResult|SCDONE
n|sourceData.verificationResults[5].cuid|60268391
c|sourceData.verificationResults[6].activityCode|FRAUD_MATCHING
c|sourceData.verificationResults[6].activityResult|DONE
n|sourceData.verificationResults[6].cuid|60268391
c|sourceData.verificationResults[7].activityCode|FPS_DATA
c|sourceData.verificationResults[7].activityResult|OK
n|sourceData.verificationResults[7].cuid|60268391
c|sourceData.verificationResults[8].activityCode|wflow.afs.send.data
c|sourceData.verificationResults[8].activityResult|OK
n|sourceData.verificationResults[8].cuid|60268391
c|sourceData.verificationResults[9].activityCode|wflow.suspend.process
c|sourceData.verificationResults[9].activityResult|DONE
n|sourceData.verificationResults[9].cuid|60268391
c|sourceData.verificationResults[10].activityCode|FPS_FLAG
c|sourceData.verificationResults[10].activityResult|OK
n|sourceData.verificationResults[10].cuid|60268391
c|sourceData.verificationResults[11].activityCode|FPS_RESPONSE_CHECK
c|sourceData.verificationResults[11].activityResult|RESCH_RNRY
n|sourceData.verificationResults[11].cuid|60268391
c|sourceData.verificationResults[12].activityCode|wflow.suspend.process
c|sourceData.verificationResults[12].activityResult|DONE
n|sourceData.verificationResults[12].cuid|60268391
c|sourceData.verificationResults[13].activityCode|FPS_RESPONSE_CHECK
c|sourceData.verificationResults[13].activityResult|RESCH_RR
n|sourceData.verificationResults[13].cuid|60268391
c|sourceData.verificationResults[14].activityCode|automatic.cb.cre
c|sourceData.verificationResults[14].activityResult|CBR_CFDB
n|sourceData.verificationResults[14].cuid|60268391
c|sourceData.verificationResults[15].activityCode|automatic.cb.cre
c|sourceData.verificationResults[15].activityResult|CBR_CFDB
n|sourceData.verificationResults[15].cuid|60268391
c|sourceData.verificationResults[16].activityCode|wflow.suspend.process
c|sourceData.verificationResults[16].activityResult|DONE
n|sourceData.verificationResults[16].cuid|60268391
c|sourceData.verificationResults[17].activityCode|big.data.check
c|sourceData.verificationResults[17].activityResult|BDOK
n|sourceData.verificationResults[17].cuid|60268391
n|workflow.stageCounters[31].WFSTAGE_INDEX|1
n|workflow.stageCounters[32].WFSTAGE_INDEX|1
n|workflow.stageCounters[33].WFSTAGE_INDEX|1
n|workflow.stageCounters[34].WFSTAGE_INDEX|1
n|workflow.stageCounters[35].WFSTAGE_INDEX|1
n|workflow.stageCounters[36].WFSTAGE_INDEX|1
n|workflow.stageCounters[37].WFSTAGE_INDEX|1
n|outputData.checkPersons[4].cuid|60268391
c|outputData.checkPersons[4].workflowCode|REJECT
n|outputData.offers[0].annuity_Max|-371
n|outputData.offers[0].baseAmount_Max|-4452
c|outputData.offers[0].offerType|SS
c|outputData.offers[0].purchaseSegment|Electronics
n|outputData.offers[1].annuity_Max|-371
n|outputData.offers[1].baseAmount_Max|-4452
c|outputData.offers[1].offerType|SS
c|outputData.offers[1].purchaseSegment|Furniture
n|outputData.offers[2].annuity_Max|-371
n|outputData.offers[2].baseAmount_Max|-4452
c|outputData.offers[2].offerType|SS
c|outputData.offers[2].purchaseSegment|Clothing
n|outputData.offers[3].annuity_Max|-371
n|outputData.offers[3].baseAmount_Max|-4452
c|outputData.offers[3].offerType|SS
c|outputData.offers[3].purchaseSegment|MobileJewelry
n|outputData.offers[4].annuity_Max|-371
n|outputData.offers[4].baseAmount_Max|-4452
c|outputData.offers[4].offerType|SS
c|outputData.offers[4].purchaseSegment|Universal
n|outputData.resultTrace[4].cuid|60268391
c|outputData.resultTrace[4].resultName|scoResult
n|outputData.uwInfo[0].annuitySum|0
n|outputData.uwInfo[0].annuitySumPaidActive|0
n|outputData.uwInfo[0].annuitySumPaidCBActive|0
n|outputData.uwInfo[0].cred_ratio|0
n|outputData.uwInfo[0].productMinAnnuity|0
n|outputData.uwInfo[0].totalDebtAmount|0
n|outputData.uwInfo[0].totalLoanAmount|0
c|scoResult.finalRiskGroup|0
c|scoResult.rejectReasonClient|CBACTDEL
c|scoResult.riskGroup|9
c|scoResult.strategyName|POS New
c|scoResult.strategyPassLog|UNEMPLOYED;SELLER;AP;HIGH_PTI;SPLITCALL;CL_PRICE_CHAMPION;SMDATA_MAILGEO_REG;SMDATA_MTSGEO_REG;ACQ_XGB_4_201907;SOFT_MODERATE
c|scoResult.strategyType|Champion
c|scoResult.strategyVersion|01.05.2016
c|scoResult.strategyVersionDate|5/12/20 2:41 PM
c|scoResult.workflowCode|REJECT
n|scoResult.appChars.bki.est_income|31936.87
d|scoResult.appChars.bki.report_date|14.05.2020 00:00:00
n|scoResult.appChars.incomes[0].est_income|31936.87
c|scoResult.appChars.incomes[0].income_type|bki
d|scoResult.appChars.incomes[0].report_date|14.05.2020 00:00:00
n|scoResult.appChars.incomes[1].est_income|28372
c|scoResult.appChars.incomes[1].income_type|regionMedian
d|scoResult.appChars.incomes[1].report_date|14.05.2020 00:00:00
n|scoResult.appChars.incomes[2].est_income|31936
c|scoResult.appChars.incomes[2].income_type|est_confirmedIncome
d|scoResult.appChars.incomes[2].report_date|14.05.2020 00:00:00
n|scoResult.blazeStatusItems[0].code|302
n|scoResult.blazeStatusItems[0].cuid|60268391
c|scoResult.blazeStatusItems[0].description|Characteristic value was 'unexpected': Characteristic name=[cbactdel], value=[1.0], score=[0.0]. 
n|scoResult.blazeStatusItems[1].code|302
n|scoResult.blazeStatusItems[1].cuid|60268391
c|scoResult.blazeStatusItems[1].description|Characteristic value was 'unexpected': Characteristic name=[cbmaxagrmnths_3_6], value=[0.0], score=[0.0]. 
n|scoResult.blazeStatusItems[2].code|302
n|scoResult.blazeStatusItems[2].cuid|60268391
c|scoResult.blazeStatusItems[2].description|Characteristic value was 'unexpected': Characteristic name=[cbmaxdpd12], value=[0.0], score=[0.0]. 
n|scoResult.blazeStatusItems[3].code|302
n|scoResult.blazeStatusItems[3].cuid|60268391
c|scoResult.blazeStatusItems[3].description|Characteristic value was 'unexpected': Characteristic name=[cbmaxdpd36], value=[0.0], score=[0.0]. 
n|scoResult.blazeStatusItems[4].code|302
n|scoResult.blazeStatusItems[4].cuid|60268391
c|scoResult.blazeStatusItems[4].description|Characteristic value was 'unexpected': Characteristic name=[annuityToCreditCur], value=[0.04267], score=[0.0]. 
n|scoResult.blazeStatusItems[5].code|302
n|scoResult.blazeStatusItems[5].cuid|60268391
c|scoResult.blazeStatusItems[5].description|Characteristic value was 'unexpected': Characteristic name=[avgAmtCredit], value=[34984.0], score=[0.0]. 
n|scoResult.blazeStatusItems[6].code|302
n|scoResult.blazeStatusItems[6].cuid|60268391
c|scoResult.blazeStatusItems[6].description|Characteristic value was 'unexpected': Characteristic name=[cntDayLastCr], value=[24.0], score=[0.0]. 
n|scoResult.blazeStatusItems[7].code|302
n|scoResult.blazeStatusItems[7].cuid|60268391
c|scoResult.blazeStatusItems[7].description|Characteristic value was 'unexpected': Characteristic name=[cntDayLastCreditCard], value=[24], score=[0.0]. 
n|scoResult.blazeStatusItems[8].code|302
n|scoResult.blazeStatusItems[8].cuid|60268391
c|scoResult.blazeStatusItems[8].description|Characteristic value was 'unexpected': Characteristic name=[cntDpd0], value=[43.0], score=[0.0]. 
n|scoResult.blazeStatusItems[9].code|302
n|scoResult.blazeStatusItems[9].cuid|60268391
c|scoResult.blazeStatusItems[9].description|Characteristic value was 'unexpected': Characteristic name=[credLength], value=[4017.0], score=[0.0]. 
n|scoResult.blazeStatusItems[10].code|302
n|scoResult.blazeStatusItems[10].cuid|60268391
c|scoResult.blazeStatusItems[10].description|Characteristic value was 'unexpected': Characteristic name=[currentCardUtilization], value=[1.0344857142857142], score=[0.0]. 
n|scoResult.blazeStatusItems[11].code|302
n|scoResult.blazeStatusItems[11].cuid|60268391
c|scoResult.blazeStatusItems[11].description|Characteristic value was 'unexpected': Characteristic name=[maxAmtReceivableCur], value=[60929.0], score=[0.0]. 
n|scoResult.blazeStatusItems[12].code|302
n|scoResult.blazeStatusItems[12].cuid|60268391
c|scoResult.blazeStatusItems[12].description|Characteristic value was 'unexpected': Characteristic name=[maxDpd6], value=[1.0], score=[0.0]. 
n|scoResult.blazeStatusItems[13].code|302
n|scoResult.blazeStatusItems[13].cuid|60268391
c|scoResult.blazeStatusItems[13].description|Characteristic value was 'unexpected': Characteristic name=[maxDpdEverCB], value=[1.0], score=[0.0]. 
n|scoResult.blazeStatusItems[14].code|302
n|scoResult.blazeStatusItems[14].cuid|60268391
c|scoResult.blazeStatusItems[14].description|Characteristic value was 'unexpected': Characteristic name=[maxLthWoPd12], value=[11.0], score=[0.0]. 
n|scoResult.blazeStatusItems[15].code|302
n|scoResult.blazeStatusItems[15].cuid|60268391
c|scoResult.blazeStatusItems[15].description|Characteristic value was 'unexpected': Characteristic name=[maxLthWoPd36], value=[19], score=[0.0]. 
n|scoResult.blazeStatusItems[16].code|302
n|scoResult.blazeStatusItems[16].cuid|60268391
c|scoResult.blazeStatusItems[16].description|Characteristic value was 'unexpected': Characteristic name=[monthsTillFreedomBur], value=[57.0], score=[0.0]. 
n|scoResult.blazeStatusItems[17].code|302
n|scoResult.blazeStatusItems[17].cuid|60268391
c|scoResult.blazeStatusItems[17].description|Characteristic value was 'unexpected': Characteristic name=[ReceivableToCreditCur], value=[0.607], score=[0.0]. 
n|scoResult.blazeStatusItems[18].code|302
n|scoResult.blazeStatusItems[18].cuid|60268391
c|scoResult.blazeStatusItems[18].description|Characteristic value was 'unexpected': Characteristic name=[sumAmtCredit], value=[664698.0], score=[0.0]. 
n|scoResult.blazeStatusItems[19].code|302
n|scoResult.blazeStatusItems[19].cuid|60268391
c|scoResult.blazeStatusItems[19].description|Characteristic value was 'unexpected': Characteristic name=[ageYearsReal], value=[56.0], score=[unknown]. 
n|scoResult.blazeStatusItems[20].code|302
n|scoResult.blazeStatusItems[20].cuid|60268391
c|scoResult.blazeStatusItems[20].description|Characteristic value was 'unexpected': Characteristic name=[flagDayTime], value=[1], score=[unknown]. 
n|scoResult.blazeStatusItems[21].code|302
n|scoResult.blazeStatusItems[21].cuid|60268391
c|scoResult.blazeStatusItems[21].description|Characteristic value was 'unexpected': Characteristic name=[flagFriendDefault], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[22].code|302
n|scoResult.blazeStatusItems[22].cuid|60268391
c|scoResult.blazeStatusItems[22].description|Characteristic value was 'unexpected': Characteristic name=[flagWeekendHol], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[23].code|302
n|scoResult.blazeStatusItems[23].cuid|60268391
c|scoResult.blazeStatusItems[23].description|Characteristic value was 'unexpected': Characteristic name=[organization_sco_group_xgb], value=[Best], score=[unknown]. 
n|scoResult.blazeStatusItems[24].code|302
n|scoResult.blazeStatusItems[24].cuid|60268391
c|scoResult.blazeStatusItems[24].description|Characteristic value was 'unexpected': Characteristic name=[employmentLenghFullMonths], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[25].code|302
n|scoResult.blazeStatusItems[25].cuid|60268391
c|scoResult.blazeStatusItems[25].description|Characteristic value was 'unexpected': Characteristic name=[avgAmtCredit], value=[34984.0], score=[unknown]. 
n|scoResult.blazeStatusItems[26].code|302
n|scoResult.blazeStatusItems[26].cuid|60268391
c|scoResult.blazeStatusItems[26].description|Characteristic value was 'unexpected': Characteristic name=[avgCredLengthCashPos], value=[662.625], score=[unknown]. 
n|scoResult.blazeStatusItems[27].code|302
n|scoResult.blazeStatusItems[27].cuid|60268391
c|scoResult.blazeStatusItems[27].description|Characteristic value was 'unexpected': Characteristic name=[cntDayLastCreditCard], value=[24], score=[unknown]. 
n|scoResult.blazeStatusItems[28].code|302
n|scoResult.blazeStatusItems[28].cuid|60268391
c|scoResult.blazeStatusItems[28].description|Characteristic value was 'unexpected': Characteristic name=[cntDpd0PlEvTall], value=[0.055], score=[unknown]. 
n|scoResult.blazeStatusItems[29].code|302
n|scoResult.blazeStatusItems[29].cuid|60268391
c|scoResult.blazeStatusItems[29].description|Characteristic value was 'unexpected': Characteristic name=[cntMonthsLastDelay], value=[2], score=[unknown]. 
n|scoResult.blazeStatusItems[30].code|302
n|scoResult.blazeStatusItems[30].cuid|60268391
c|scoResult.blazeStatusItems[30].description|Characteristic value was 'unexpected': Characteristic name=[maxAmtCredit], value=[106600.0], score=[unknown]. 
n|scoResult.blazeStatusItems[31].code|302
n|scoResult.blazeStatusItems[31].cuid|60268391
c|scoResult.blazeStatusItems[31].description|Characteristic value was 'unexpected': Characteristic name=[currentCardUtilization], value=[1.0344857142857142], score=[unknown]. 
n|scoResult.blazeStatusItems[32].code|302
n|scoResult.blazeStatusItems[32].cuid|60268391
c|scoResult.blazeStatusItems[32].description|Characteristic value was 'unexpected': Characteristic name=[maxDpdEverCB], value=[1.0], score=[unknown]. 
n|scoResult.blazeStatusItems[33].code|302
n|scoResult.blazeStatusItems[33].cuid|60268391
c|scoResult.blazeStatusItems[33].description|Characteristic value was 'unexpected': Characteristic name=[minAmtCreditCur], value=[5000.0], score=[unknown]. 
n|scoResult.blazeStatusItems[34].code|302
n|scoResult.blazeStatusItems[34].cuid|60268391
c|scoResult.blazeStatusItems[34].description|Characteristic value was 'unexpected': Characteristic name=[monthsTillFreedomBur], value=[57.0], score=[unknown]. 
n|scoResult.blazeStatusItems[35].code|302
n|scoResult.blazeStatusItems[35].cuid|60268391
c|scoResult.blazeStatusItems[35].description|Characteristic value was 'unexpected': Characteristic name=[ReceivableToCreditCur], value=[0.607], score=[unknown]. 
n|scoResult.blazeStatusItems[36].code|302
n|scoResult.blazeStatusItems[36].cuid|60268391
c|scoResult.blazeStatusItems[36].description|Characteristic value was 'unexpected': Characteristic name=[sumRecCurCashPos], value=[165313.46], score=[unknown]. 
n|scoResult.blazeStatusItems[37].code|302
n|scoResult.blazeStatusItems[37].cuid|60268391
c|scoResult.blazeStatusItems[37].description|Characteristic value was 'unexpected': Characteristic name=[score_beeline_new_comp], value=[0.9675186245391769], score=[unknown]. 
n|scoResult.blazeStatusItems[38].code|302
n|scoResult.blazeStatusItems[38].cuid|60268391
c|scoResult.blazeStatusItems[38].description|Characteristic value was 'unexpected': Characteristic name=[score_beeline_new_comp_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[39].code|302
n|scoResult.blazeStatusItems[39].cuid|60268391
c|scoResult.blazeStatusItems[39].description|Characteristic value was 'unexpected': Characteristic name=[score_beeline_new_cl], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[40].code|302
n|scoResult.blazeStatusItems[40].cuid|60268391
c|scoResult.blazeStatusItems[40].description|Characteristic value was 'unexpected': Characteristic name=[score_beeline_new_cl_f], value=[1], score=[unknown]. 
n|scoResult.blazeStatusItems[41].code|302
n|scoResult.blazeStatusItems[41].cuid|60268391
c|scoResult.blazeStatusItems[41].description|Characteristic value was 'unexpected': Characteristic name=[score_equif], value=[687.0], score=[unknown]. 
n|scoResult.blazeStatusItems[42].code|302
n|scoResult.blazeStatusItems[42].cuid|60268391
c|scoResult.blazeStatusItems[42].description|Characteristic value was 'unexpected': Characteristic name=[score_equif_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[43].code|302
n|scoResult.blazeStatusItems[43].cuid|60268391
c|scoResult.blazeStatusItems[43].description|Characteristic value was 'unexpected': Characteristic name=[score_fps_afs], value=[0.9587332819883743], score=[unknown]. 
n|scoResult.blazeStatusItems[44].code|302
n|scoResult.blazeStatusItems[44].cuid|60268391
c|scoResult.blazeStatusItems[44].description|Characteristic value was 'unexpected': Characteristic name=[score_fps_afs_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[45].code|302
n|scoResult.blazeStatusItems[45].cuid|60268391
c|scoResult.blazeStatusItems[45].description|Characteristic value was 'unexpected': Characteristic name=[mail_geo_work_work], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[46].code|302
n|scoResult.blazeStatusItems[46].cuid|60268391
c|scoResult.blazeStatusItems[46].description|Characteristic value was 'unexpected': Characteristic name=[mail_geo_work_work_f], value=[1.0], score=[unknown]. 
n|scoResult.blazeStatusItems[47].code|302
n|scoResult.blazeStatusItems[47].cuid|60268391
c|scoResult.blazeStatusItems[47].description|Characteristic value was 'unexpected': Characteristic name=[mail_geo_reg_home], value=[0.7913591869], score=[unknown]. 
n|scoResult.blazeStatusItems[48].code|302
n|scoResult.blazeStatusItems[48].cuid|60268391
c|scoResult.blazeStatusItems[48].description|Characteristic value was 'unexpected': Characteristic name=[mail_geo_reg_home_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[49].code|302
n|scoResult.blazeStatusItems[49].cuid|60268391
c|scoResult.blazeStatusItems[49].description|Characteristic value was 'unexpected': Characteristic name=[score_meg_cl], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[50].code|302
n|scoResult.blazeStatusItems[50].cuid|60268391
c|scoResult.blazeStatusItems[50].description|Characteristic value was 'unexpected': Characteristic name=[score_meg_cl_f], value=[1], score=[unknown]. 
n|scoResult.blazeStatusItems[51].code|302
n|scoResult.blazeStatusItems[51].cuid|60268391
c|scoResult.blazeStatusItems[51].description|Characteristic value was 'unexpected': Characteristic name=[score_meg_comp], value=[0.9212217], score=[unknown]. 
n|scoResult.blazeStatusItems[52].code|302
n|scoResult.blazeStatusItems[52].cuid|60268391
c|scoResult.blazeStatusItems[52].description|Characteristic value was 'unexpected': Characteristic name=[score_meg_comp_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[53].code|302
n|scoResult.blazeStatusItems[53].cuid|60268391
c|scoResult.blazeStatusItems[53].description|Characteristic value was 'unexpected': Characteristic name=[score_mts_cl], value=[0.94588772], score=[unknown]. 
n|scoResult.blazeStatusItems[54].code|302
n|scoResult.blazeStatusItems[54].cuid|60268391
c|scoResult.blazeStatusItems[54].description|Characteristic value was 'unexpected': Characteristic name=[score_mts_cl_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[55].code|302
n|scoResult.blazeStatusItems[55].cuid|60268391
c|scoResult.blazeStatusItems[55].description|Characteristic value was 'unexpected': Characteristic name=[score_mts_comp], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[56].code|302
n|scoResult.blazeStatusItems[56].cuid|60268391
c|scoResult.blazeStatusItems[56].description|Characteristic value was 'unexpected': Characteristic name=[score_mts_comp_f], value=[1], score=[unknown]. 
n|scoResult.blazeStatusItems[57].code|302
n|scoResult.blazeStatusItems[57].cuid|60268391
c|scoResult.blazeStatusItems[57].description|Characteristic value was 'unexpected': Characteristic name=[score_tele2], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[58].code|302
n|scoResult.blazeStatusItems[58].cuid|60268391
c|scoResult.blazeStatusItems[58].description|Characteristic value was 'unexpected': Characteristic name=[score_tele2_f], value=[1], score=[unknown]. 
n|scoResult.blazeStatusItems[59].code|302
n|scoResult.blazeStatusItems[59].cuid|60268391
c|scoResult.blazeStatusItems[59].description|Characteristic value was 'unexpected': Characteristic name=[score_exp], value=[978.0], score=[unknown]. 
n|scoResult.blazeStatusItems[60].code|302
n|scoResult.blazeStatusItems[60].cuid|60268391
c|scoResult.blazeStatusItems[60].description|Characteristic value was 'unexpected': Characteristic name=[score_exp_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[61].code|302
n|scoResult.blazeStatusItems[61].cuid|60268391
c|scoResult.blazeStatusItems[61].description|Characteristic value was 'unexpected': Characteristic name=[score_yandex], value=[unavailable], score=[unknown]. 
n|scoResult.blazeStatusItems[62].code|302
n|scoResult.blazeStatusItems[62].cuid|60268391
c|scoResult.blazeStatusItems[62].description|Characteristic value was 'unexpected': Characteristic name=[score_yandex_f], value=[1], score=[unknown]. 
n|scoResult.blazeStatusItems[63].code|302
n|scoResult.blazeStatusItems[63].cuid|60268391
c|scoResult.blazeStatusItems[63].description|Characteristic value was 'unexpected': Characteristic name=[score_soc_circle], value=[633.0], score=[unknown]. 
n|scoResult.blazeStatusItems[64].code|302
n|scoResult.blazeStatusItems[64].cuid|60268391
c|scoResult.blazeStatusItems[64].description|Characteristic value was 'unexpected': Characteristic name=[score_soc_circle_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[65].code|302
n|scoResult.blazeStatusItems[65].cuid|60268391
c|scoResult.blazeStatusItems[65].description|Characteristic value was 'unexpected': Characteristic name=[score_mail], value=[0.6006865587], score=[unknown]. 
n|scoResult.blazeStatusItems[66].code|302
n|scoResult.blazeStatusItems[66].cuid|60268391
c|scoResult.blazeStatusItems[66].description|Characteristic value was 'unexpected': Characteristic name=[score_mail_f], value=[0], score=[unknown]. 
n|scoResult.blazeStatusItems[67].code|302
n|scoResult.blazeStatusItems[67].cuid|60268391
c|scoResult.blazeStatusItems[67].description|Characteristic value was 'unexpected': Characteristic name=[score_bureau_f], value=[0], score=[unknown]. 
n|scoResult.client.adjustedIncome|25000
n|scoResult.client.availableForSale|1
n|scoResult.client.cbAnnuity|16025.104197327177
n|scoResult.client.cbDebt|156707
n|scoResult.client.cbDebtRDneverUsed|0
n|scoResult.client.cbDebtUsed|156707
n|scoResult.client.confirmedIncome|31936
n|scoResult.client.estimatedFamilyIncome|25000
c|scoResult.client.income_type|bki
c|scoResult.client.processLine|SPLITCALL;CL_PRICE_CHAMPION;SOFT_MODERATE
n|scoResult.client.regionalAvailableAnnuity|-5920
n|scoResult.client.regulatorAppIncomeAvailableAnnuity|-5920
n|scoResult.client.regulatorAppIncomeToUwAvailableAnnuity|-5920
n|scoResult.client.regulatorAvailableAnnuity|-371
n|scoResult.client.regulatorCBAnnuity|25920.50971296496
n|scoResult.client.regulatorHCFBcashCBAnnuity|0
c|scoResult.client.riskSet|omega
n|scoResult.derivedData.persons[0].cuid|60268391
n|scoResult.derivedData.persons[0].undesirablePeriod|0
c|scoResult.hardChecksResults[0].koCode|CBACTDEL
n|scoResult.limit.persons[0].cuid|60268391
n|scoResult.limit.persons[0].dtiLimit|-4452
n|scoResult.limit.persons[0].finalLimit|-4452
n|scoResult.limit.persons[0].limitResult|0
n|scoResult.persons[0].cuid|60268391
c|scoResult.persons[0].rejectReason|HC
n|scoResult.score.score17|0.9587332819883743
c|scoResult.score.score17Function|FPSAFS_1812
n|scoResult.score.score22|0.8957098216909815
c|scoResult.score.score22Function|Bureau_XGB_4_201910
n|scoResult.score.score9|0.8808115656067731
c|scoResult.score.score9Function|ACQ_XGB_4_201907
n|scoResult.score.persons[0].cuid|60268391
c|scoResult.score.persons[0].lineID|REJ_OMEGA_ANTICRISIS
n|scoResult.score.persons[0].scoreEnd1|0.8808115656067731
c|scoResult.score.persons[0].scoreFunction|ACQ_XGB_4_201907
c|scoResult.score22Predictors[0].predictorCode|cbactdel
n|scoResult.score22Predictors[0].predictorScore|0
c|scoResult.score22Predictors[0].predictorValue|1.0
c|scoResult.score22Predictors[1].predictorCode|cbmaxagrmnths_3_6
n|scoResult.score22Predictors[1].predictorScore|0
c|scoResult.score22Predictors[1].predictorValue|0.0
c|scoResult.score22Predictors[2].predictorCode|cbmaxdpd12
n|scoResult.score22Predictors[2].predictorScore|0
c|scoResult.score22Predictors[2].predictorValue|0.0
c|scoResult.score22Predictors[3].predictorCode|cbmaxdpd36
n|scoResult.score22Predictors[3].predictorScore|0
c|scoResult.score22Predictors[3].predictorValue|0.0
c|scoResult.score22Predictors[4].predictorCode|annuityToCreditCur
n|scoResult.score22Predictors[4].predictorScore|0
c|scoResult.score22Predictors[4].predictorValue|0.04267
c|scoResult.score22Predictors[5].predictorCode|avgAmtCredit
n|scoResult.score22Predictors[5].predictorScore|0
c|scoResult.score22Predictors[5].predictorValue|34984.0
c|scoResult.score22Predictors[6].predictorCode|cntDayLastCr
n|scoResult.score22Predictors[6].predictorScore|0
c|scoResult.score22Predictors[6].predictorValue|24.0
c|scoResult.score22Predictors[7].predictorCode|cntDayLastCreditCard
n|scoResult.score22Predictors[7].predictorScore|0
c|scoResult.score22Predictors[7].predictorValue|24
c|scoResult.score22Predictors[8].predictorCode|cntDpd0
n|scoResult.score22Predictors[8].predictorScore|0
c|scoResult.score22Predictors[8].predictorValue|43.0
c|scoResult.score22Predictors[9].predictorCode|credLength
n|scoResult.score22Predictors[9].predictorScore|0
c|scoResult.score22Predictors[9].predictorValue|4017.0
c|scoResult.score22Predictors[10].predictorCode|currentCardUtilization
n|scoResult.score22Predictors[10].predictorScore|0
c|scoResult.score22Predictors[10].predictorValue|1.0344857142857142
c|scoResult.score22Predictors[11].predictorCode|maxAmtReceivableCur
n|scoResult.score22Predictors[11].predictorScore|0
c|scoResult.score22Predictors[11].predictorValue|60929.0
c|scoResult.score22Predictors[12].predictorCode|maxDpd6
n|scoResult.score22Predictors[12].predictorScore|0
c|scoResult.score22Predictors[12].predictorValue|1.0
c|scoResult.score22Predictors[13].predictorCode|maxDpdEverCB
n|scoResult.score22Predictors[13].predictorScore|0
c|scoResult.score22Predictors[13].predictorValue|1.0
c|scoResult.score22Predictors[14].predictorCode|maxLthWoPd12
n|scoResult.score22Predictors[14].predictorScore|0
c|scoResult.score22Predictors[14].predictorValue|11.0
c|scoResult.score22Predictors[15].predictorCode|maxLthWoPd36
n|scoResult.score22Predictors[15].predictorScore|0
c|scoResult.score22Predictors[15].predictorValue|19
c|scoResult.score22Predictors[16].predictorCode|monthsTillFreedomBur
n|scoResult.score22Predictors[16].predictorScore|0
c|scoResult.score22Predictors[16].predictorValue|57.0
c|scoResult.score22Predictors[17].predictorCode|ReceivableToCreditCur
n|scoResult.score22Predictors[17].predictorScore|0
c|scoResult.score22Predictors[17].predictorValue|0.607
c|scoResult.score22Predictors[18].predictorCode|sumAmtCredit
n|scoResult.score22Predictors[18].predictorScore|0
c|scoResult.score22Predictors[18].predictorValue|664698.0
c|scoResult.score9Predictors[0].predictorCode|ageYearsReal
c|scoResult.score9Predictors[0].predictorValue|56.0
c|scoResult.score9Predictors[1].predictorCode|flagDayTime
c|scoResult.score9Predictors[1].predictorValue|1
c|scoResult.score9Predictors[2].predictorCode|flagFriendDefault
c|scoResult.score9Predictors[3].predictorCode|flagWeekendHol
c|scoResult.score9Predictors[3].predictorValue|0
c|scoResult.score9Predictors[4].predictorCode|organization_sco_group_xgb
c|scoResult.score9Predictors[4].predictorValue|Best
c|scoResult.score9Predictors[5].predictorCode|employmentLenghFullMonths
c|scoResult.score9Predictors[6].predictorCode|avgAmtCredit
c|scoResult.score9Predictors[6].predictorValue|34984.0
c|scoResult.score9Predictors[7].predictorCode|avgCredLengthCashPos
c|scoResult.score9Predictors[7].predictorValue|662.625
c|scoResult.score9Predictors[8].predictorCode|cntDayLastCreditCard
c|scoResult.score9Predictors[8].predictorValue|24
c|scoResult.score9Predictors[9].predictorCode|cntDpd0PlEvTall
c|scoResult.score9Predictors[9].predictorValue|0.055
c|scoResult.score9Predictors[10].predictorCode|cntMonthsLastDelay
c|scoResult.score9Predictors[10].predictorValue|2
c|scoResult.score9Predictors[11].predictorCode|maxAmtCredit
c|scoResult.score9Predictors[11].predictorValue|106600.0
c|scoResult.score9Predictors[12].predictorCode|currentCardUtilization
c|scoResult.score9Predictors[12].predictorValue|1.0344857142857142
c|scoResult.score9Predictors[13].predictorCode|maxDpdEverCB
c|scoResult.score9Predictors[13].predictorValue|1.0
c|scoResult.score9Predictors[14].predictorCode|minAmtCreditCur
c|scoResult.score9Predictors[14].predictorValue|5000.0
c|scoResult.score9Predictors[15].predictorCode|monthsTillFreedomBur
c|scoResult.score9Predictors[15].predictorValue|57.0
c|scoResult.score9Predictors[16].predictorCode|ReceivableToCreditCur
c|scoResult.score9Predictors[16].predictorValue|0.607
c|scoResult.score9Predictors[17].predictorCode|sumRecCurCashPos
c|scoResult.score9Predictors[17].predictorValue|165313.46
c|scoResult.score9Predictors[18].predictorCode|score_beeline_new_comp
c|scoResult.score9Predictors[18].predictorValue|0.9675186245391769
c|scoResult.score9Predictors[19].predictorCode|score_beeline_new_comp_f
c|scoResult.score9Predictors[19].predictorValue|0
c|scoResult.score9Predictors[20].predictorCode|score_beeline_new_cl
c|scoResult.score9Predictors[21].predictorCode|score_beeline_new_cl_f
c|scoResult.score9Predictors[21].predictorValue|1
c|scoResult.score9Predictors[22].predictorCode|score_equif
c|scoResult.score9Predictors[22].predictorValue|687.0
c|scoResult.score9Predictors[23].predictorCode|score_equif_f
c|scoResult.score9Predictors[23].predictorValue|0
c|scoResult.score9Predictors[24].predictorCode|score_fps_afs
c|scoResult.score9Predictors[24].predictorValue|0.9587332819883743
c|scoResult.score9Predictors[25].predictorCode|score_fps_afs_f
c|scoResult.score9Predictors[25].predictorValue|0
c|scoResult.score9Predictors[26].predictorCode|mail_geo_work_work
c|scoResult.score9Predictors[27].predictorCode|mail_geo_work_work_f
c|scoResult.score9Predictors[27].predictorValue|1.0
c|scoResult.score9Predictors[28].predictorCode|mail_geo_reg_home
c|scoResult.score9Predictors[28].predictorValue|0.7913591869
c|scoResult.score9Predictors[29].predictorCode|mail_geo_reg_home_f
c|scoResult.score9Predictors[29].predictorValue|0
c|scoResult.score9Predictors[30].predictorCode|score_meg_cl
c|scoResult.score9Predictors[31].predictorCode|score_meg_cl_f
c|scoResult.score9Predictors[31].predictorValue|1
c|scoResult.score9Predictors[32].predictorCode|score_meg_comp
c|scoResult.score9Predictors[32].predictorValue|0.9212217
c|scoResult.score9Predictors[33].predictorCode|score_meg_comp_f
c|scoResult.score9Predictors[33].predictorValue|0
c|scoResult.score9Predictors[34].predictorCode|score_mts_cl
c|scoResult.score9Predictors[34].predictorValue|0.94588772
c|scoResult.score9Predictors[35].predictorCode|score_mts_cl_f
c|scoResult.score9Predictors[35].predictorValue|0
c|scoResult.score9Predictors[36].predictorCode|score_mts_comp
c|scoResult.score9Predictors[37].predictorCode|score_mts_comp_f
c|scoResult.score9Predictors[37].predictorValue|1
c|scoResult.score9Predictors[38].predictorCode|score_tele2
c|scoResult.score9Predictors[39].predictorCode|score_tele2_f
c|scoResult.score9Predictors[39].predictorValue|1
c|scoResult.score9Predictors[40].predictorCode|score_exp
c|scoResult.score9Predictors[40].predictorValue|978.0
c|scoResult.score9Predictors[41].predictorCode|score_exp_f
c|scoResult.score9Predictors[41].predictorValue|0
c|scoResult.score9Predictors[42].predictorCode|score_yandex
c|scoResult.score9Predictors[43].predictorCode|score_yandex_f
c|scoResult.score9Predictors[43].predictorValue|1
c|scoResult.score9Predictors[44].predictorCode|score_soc_circle
c|scoResult.score9Predictors[44].predictorValue|633.0
c|scoResult.score9Predictors[45].predictorCode|score_soc_circle_f
c|scoResult.score9Predictors[45].predictorValue|0
c|scoResult.score9Predictors[46].predictorCode|score_mail
c|scoResult.score9Predictors[46].predictorValue|0.6006865587
c|scoResult.score9Predictors[47].predictorCode|score_mail_f
c|scoResult.score9Predictors[47].predictorValue|0
c|scoResult.score9Predictors[48].predictorCode|score_bureau_f
c|scoResult.score9Predictors[48].predictorValue|0
n|workflow.stageCounters[34].WFSTAGE_INDEX|1
n|workflow.stageCounters[16].WFSTAGE_INDEX|1
n|workflow.stageCounters[17].WFSTAGE_INDEX|1
n|workflow.stageCounters[35].WFSTAGE_INDEX|1
n|workflow.stageCounters[36].WFSTAGE_INDEX|1
n|workflow.stageCounters[37].WFSTAGE_INDEX|1
n|workflow.stageCounters[55].WFSTAGE_INDEX|2241
n|workflow.stageCounters[56].WFSTAGE_INDEX|8311
n|workflow.stageCounters[57].WFSTAGE_INDEX|8309
n|workflow.stageCounters[58].WFSTAGE_INDEX|8310
n|workflow.stageCounters[59].WFSTAGE_INDEX|7115
c|credit.fps.responseStatusApplication|0
c|credit.fps.responseStatusPhoto|0
n|workflow.stageCounters[18].WFSTAGE_INDEX|1
n|workflow.stageCounters[19].WFSTAGE_INDEX|1
n|workflow.stageCounters[20].WFSTAGE_INDEX|1
n|workflow.stageCounters[60].WFSTAGE_INDEX|8509
n|workflow.stageCounters[61].WFSTAGE_INDEX|3377
n|workflow.stageCounters[62].WFSTAGE_INDEX|6799
c|predictorsList[0].name|MAX_DATE_OPEN_CARD
c|predictorsList[1].name|CNT_CLOSED_CASH_POS
c|predictorsList[2].name|AGE_YEARS_REAL
c|predictorsList[3].name|EDUCATION
c|predictorsList[4].name|ALL_CASH_POS
c|predictorsList[5].name|CB_MAXAGRMNTHS_1_3
c|predictorsList[6].name|CB_MAXAGRMNTHS_2_3
c|predictorsList[7].name|CB_MAXAGRMNTHS_3_3
'''

# n|sourceData.behaviourData.persons[0].FlagNoInstNoPmt36M|0
# c|sourceData.behaviourData.persons[0].altContactType|Sister
# n|sourceData.behaviourData.persons[0].amtCreditDpd30|100000
# n|sourceData.behaviourData.persons[0].amtDpd|32128
# n|sourceData.behaviourData.persons[0].amtDpd0_24m|0
# n|sourceData.behaviourData.persons[0].amtDpd0_36m|4615
# n|sourceData.behaviourData.persons[0].amtDpd0_3m|0
# n|sourceData.behaviourData.persons[0].amtDpd0_9m|0
# n|sourceData.behaviourData.persons[0].amtDpd12m|0
# n|sourceData.behaviourData.persons[0].amtDpd30Ever|22957
# n|sourceData.behaviourData.persons[0].amtDpd30_12m|0
# n|sourceData.behaviourData.persons[0].amtDpd30_24m|0
# n|sourceData.behaviourData.persons[0].amtDpd30_36m|0
# n|sourceData.behaviourData.persons[0].amtDpd30_3m|0
# n|sourceData.behaviourData.persons[0].amtDpd30_6m|0
# n|sourceData.behaviourData.persons[0].amtDpd30_9m|0
# n|sourceData.behaviourData.persons[0].amtDpd6m|0
# n|sourceData.behaviourData.persons[0].amtFpd0|0
# n|sourceData.behaviourData.persons[0].amtFpd0_36m|0
# n|sourceData.behaviourData.persons[0].amtSpd0|0
# n|sourceData.behaviourData.persons[0].amtSpd0_36m|0
# n|sourceData.behaviourData.persons[0].amtTpd0|4556
# n|sourceData.behaviourData.persons[0].amtTpd0_36m|0
# n|sourceData.behaviourData.persons[0].averageFullEPToAnnuity|9.85539165549166231030903622216666287853
# n|sourceData.behaviourData.persons[0].avgDaysBetweenApplications|202
# n|sourceData.behaviourData.persons[0].avgDaysBetweenApplications24m|0
# n|sourceData.behaviourData.persons[0].avgDpd03m|0
# n|sourceData.behaviourData.persons[0].avgDpd0_12m|0
# n|sourceData.behaviourData.persons[0].avgDpd0_24m|0
# n|sourceData.behaviourData.persons[0].avgDpd0_36m|0.5945945945945945945945945945945945945946
# n|sourceData.behaviourData.persons[0].avgDpd0_6m|0
# n|sourceData.behaviourData.persons[0].avgDpd0_9m|0
# n|sourceData.behaviourData.persons[0].avgDpd0_ever|62.875
# n|sourceData.behaviourData.persons[0].avgDpd30|7.58333333333333333333333333333333333333
# n|sourceData.behaviourData.persons[0].avgDpd30_12m|0
# n|sourceData.behaviourData.persons[0].avgDpd30_24m|0
# n|sourceData.behaviourData.persons[0].avgDpd30_36m|0
# n|sourceData.behaviourData.persons[0].avgDpd30_3m|0
# n|sourceData.behaviourData.persons[0].avgDpd30_6m|0
# n|sourceData.behaviourData.persons[0].avgDpd30_9m|0
# n|sourceData.behaviourData.persons[0].avgDpdCurr_SC|0
# n|sourceData.behaviourData.persons[0].avgDpdCurr_SC_SS|0
# n|sourceData.behaviourData.persons[0].avgDpdTol|11
# n|sourceData.behaviourData.persons[0].avgRateLengthEP|0.58333
# c|sourceData.behaviourData.persons[0].clientType|Other
# n|sourceData.behaviourData.persons[0].cntApplication|4
# n|sourceData.behaviourData.persons[0].cntApplication24m|0
# n|sourceData.behaviourData.persons[0].cntApproved|3
# n|sourceData.behaviourData.persons[0].cntApproved24m|0
# n|sourceData.behaviourData.persons[0].cntClosed|2
# n|sourceData.behaviourData.persons[0].cntContractActiveRevolvingLinked|0
# n|sourceData.behaviourData.persons[0].cntContractActiveRevolvingPOSonCard|0
# n|sourceData.behaviourData.persons[0].cntDelay30days12m|0
# n|sourceData.behaviourData.persons[0].cntDelay30days24m|0
# n|sourceData.behaviourData.persons[0].cntDelay30days6m|0
# n|sourceData.behaviourData.persons[0].cntDelay5days12m|0
# n|sourceData.behaviourData.persons[0].cntDelay5days24m|0
# n|sourceData.behaviourData.persons[0].cntDelay5days6m|0
# n|sourceData.behaviourData.persons[0].cntDpd0|7
# n|sourceData.behaviourData.persons[0].cntDpd0_12m|0
# n|sourceData.behaviourData.persons[0].cntDpd0_24m|0
# n|sourceData.behaviourData.persons[0].cntDpd0_36m|1
# n|sourceData.behaviourData.persons[0].cntDpd0_9m|0
# n|sourceData.behaviourData.persons[0].cntDpd30Ever|5
# n|sourceData.behaviourData.persons[0].cntDpd30_3m|0
# n|sourceData.behaviourData.persons[0].cntDpd30_9m|0
# n|sourceData.behaviourData.persons[0].cntDpd3m|0
# n|sourceData.behaviourData.persons[0].cntDpd6Plus12m|0
# n|sourceData.behaviourData.persons[0].cntDpd6m|0
# n|sourceData.behaviourData.persons[0].cntDpd6to12m|0
# n|sourceData.behaviourData.persons[0].cntGoodPos|0
# n|sourceData.behaviourData.persons[0].cntInst12M|12
# n|sourceData.behaviourData.persons[0].cntInst24M|24
# n|sourceData.behaviourData.persons[0].cntInst6M|6
# n|sourceData.behaviourData.persons[0].cntRejected1m|0
# n|sourceData.behaviourData.persons[0].cntRejected24m|0
# n|sourceData.behaviourData.persons[0].cntUniquePhones|0
# n|sourceData.behaviourData.persons[0].cntUnsuccessfulWeeks24m|0
# n|sourceData.behaviourData.persons[0].cntdelay30days36m|1
# c|sourceData.behaviourData.persons[0].codePaidOffAfterDpd|2
# c|sourceData.behaviourData.persons[0].crmSegment|ACTIVE_CASH
# n|sourceData.behaviourData.persons[0].currentDebtRevolvingLinked|0
# n|sourceData.behaviourData.persons[0].currentDebtRevolvingPOSonCard|0
# d|sourceData.behaviourData.persons[0].dateIdPublish|11.06.2014 00:00:00
# d|sourceData.behaviourData.persons[0].dateLastDpd30|20.02.2017 00:00:00
# d|sourceData.behaviourData.persons[0].dateLastDpdTol|23.03.2017 00:00:00
# d|sourceData.behaviourData.persons[0].dateLastFullApplication|14.04.2017 12:50:54
# d|sourceData.behaviourData.persons[0].dateLastTpd0|18.09.2016 00:00:00
# n|sourceData.behaviourData.persons[0].difFinSituation|0
# n|sourceData.behaviourData.persons[0].dpdCurr_SC|0
# n|sourceData.behaviourData.persons[0].dpdCurr_SC_SS|0
# n|sourceData.behaviourData.persons[0].dpdCurr_SS|0
# d|sourceData.behaviourData.persons[0].employment.employedFrom|01.02.2012 00:00:00
# c|sourceData.behaviourData.persons[0].employmentAddress.region|63
# c|sourceData.behaviourData.persons[0].employmentAddress.town|сызрань
# c|sourceData.behaviourData.persons[0].familyState|5
# c|sourceData.behaviourData.persons[0].firstaGoodsCat|CT
# c|sourceData.behaviourData.persons[0].flagFriendDefault|friend
# n|sourceData.behaviourData.persons[0].flagVipSalaryClient|0
# n|sourceData.behaviourData.persons[0].floorsMaxMedi|10
# n|sourceData.behaviourData.persons[0].fullEPCount|1
# n|sourceData.behaviourData.persons[0].histDpd_1m|0
# n|sourceData.behaviourData.persons[0].histDpd_9m|0
# n|sourceData.behaviourData.persons[0].instalmentCntPaidInTime|40
# d|sourceData.behaviourData.persons[0].lastFullEPDate|16.07.2016 00:00:00
# n|sourceData.behaviourData.persons[0].lastFullEPPercent|0.923191512011639047585252475071856924879
# d|sourceData.behaviourData.persons[0].lastOfflineDate|24.03.2020 00:00:00
# d|sourceData.behaviourData.persons[0].lastPaidTotalDebtTolerance|14.04.2017 00:00:00
# n|sourceData.behaviourData.persons[0].lastPosDownpaymentRatio|0.19011
# n|sourceData.behaviourData.persons[0].maxAmtPd24m|0
# n|sourceData.behaviourData.persons[0].maxAmtPd36m|4615
# n|sourceData.behaviourData.persons[0].maxAmtPdEver|4615
# n|sourceData.behaviourData.persons[0].maxDbd_3m|18
# n|sourceData.behaviourData.persons[0].maxDpdTol|146
# n|sourceData.behaviourData.persons[0].maxDpdTol6M|0
# n|sourceData.behaviourData.persons[0].maxFpd|0
# n|sourceData.behaviourData.persons[0].maxFpd_36m|0
# n|sourceData.behaviourData.persons[0].maxRateLengthEP|0.1722222222222222222222222222222222222222
# n|sourceData.behaviourData.persons[0].maxSpd|0
# n|sourceData.behaviourData.persons[0].maxSpd_36m|0
# n|sourceData.behaviourData.persons[0].maxTpd|57
# n|sourceData.behaviourData.persons[0].maxTpd_36m|0
# n|sourceData.behaviourData.persons[0].maxannuity|85556.54
# n|sourceData.behaviourData.persons[0].maxdpd|146
# n|sourceData.behaviourData.persons[0].maxdpd12|0
# n|sourceData.behaviourData.persons[0].maxdpd24|0
# n|sourceData.behaviourData.persons[0].maxdpd36|22
# n|sourceData.behaviourData.persons[0].maxdpd48|146
# n|sourceData.behaviourData.persons[0].maxdpd6|0
# n|sourceData.behaviourData.persons[0].maxdpd60|146
# n|sourceData.behaviourData.persons[0].maxdpdLast4inst|0
# n|sourceData.behaviourData.persons[0].monthsTillFreedomO|12.70967741935483870967741935483870967742
# n|sourceData.behaviourData.persons[0].monthsannuity|45
# c|sourceData.behaviourData.persons[0].nameEmployerType|Школы
# n|sourceData.behaviourData.persons[0].numInstPaid|47
# n|sourceData.behaviourData.persons[0].numInstPaidTol|47
# n|sourceData.behaviourData.persons[0].numInstToPayGr|13
# c|sourceData.behaviourData.persons[0].occupation|Секретарь
# d|sourceData.behaviourData.persons[0].registeredAddress.dateRegistration|02.10.2003 00:00:00
# c|sourceData.behaviourData.persons[0].registeredAddress.region|73
# c|sourceData.behaviourData.persons[0].registeredAddress.town|Ульяновск
# c|sourceData.behaviourData.persons[0].sellerplaceLastPosSize|Каменные
# n|sourceData.behaviourData.persons[0].sumDpd24m|0
# n|sourceData.behaviourData.persons[0].sumDpd30Ever|455
# n|sourceData.behaviourData.persons[0].sumDpd30_12m|0
# n|sourceData.behaviourData.persons[0].sumDpd30_24m|0
# n|sourceData.behaviourData.persons[0].sumDpd30_36m|0
# n|sourceData.behaviourData.persons[0].sumDpd30_3m|0
# n|sourceData.behaviourData.persons[0].sumDpd30_6m|0
# n|sourceData.behaviourData.persons[0].sumDpd30_9m|0
# n|sourceData.behaviourData.persons[0].sumDpd6m|0
# n|sourceData.behaviourData.persons[0].sumDpdTol|503
# n|sourceData.behaviourData.persons[0].sumDpd_12m|0
# n|sourceData.behaviourData.persons[0].sumDpd_36m|22
# n|sourceData.behaviourData.persons[0].sumDpd_3m|0
# n|sourceData.behaviourData.persons[0].sumDpd_9m|0
# n|sourceData.behaviourData.persons[0].sumFpd|0
# n|sourceData.behaviourData.persons[0].sumFpd_36m|0
# n|sourceData.behaviourData.persons[0].sumPaidAmountEver|278038.23
# n|sourceData.behaviourData.persons[0].sumSpd|0
# n|sourceData.behaviourData.persons[0].sumSpd_36m|0
# n|sourceData.behaviourData.persons[0].sumTpd|57
# n|sourceData.behaviourData.persons[0].sumTpd_36m|0
# n|sourceData.behaviourData.persons[0].sumdpd|503
# n|sourceData.behaviourData.persons[0].sumloan|0.5
# c|sourceData.behaviourData.persons[0].textLastRiskProdCombination|Cash Street: low
# c|sourceData.behaviourData.persons[0].typeLastFullApplication|Cash loans
# n|sourceData.behaviourData.persons[0].uak3|3.42
# n|sourceData.behaviourData.persons[0].us3B|0
# n|sourceData.behaviourData.persons[0].cuid|60268391
# n|approvalCharacteristics[0].realValue|10
# c|approvalCharacteristics[0].name|CNT_CLOSED_CASH_POS
# c|approvalCharacteristics[0].class|scoreCardPredictor
# c|approvalCharacteristics[0].variation|1
# n|approvalCharacteristics[1].realValue|88
# c|approvalCharacteristics[1].name|AGE_YEARS_REAL
# c|approvalCharacteristics[1].class|scoreCardPredictor
# c|approvalCharacteristics[1].variation|1
# c|approvalCharacteristics[2].charValue|random
# c|approvalCharacteristics[2].name|RANDOM
# c|approvalCharacteristics[2].class|scoreCardPredictor
# c|approvalCharacteristics[2].variation|1
# n|credit.creditBureau.creditData[0].cbAnnuity|0
# c|credit.creditBureau.creditData[0].cbId|exp
# c|credit.creditBureau.creditData[0].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC-0--
# c|credit.creditBureau.creditData[0].contractSource|cb
# n|credit.creditBureau.creditData[0].cred_ratio|0
# n|credit.creditBureau.creditData[0].creditActive|0
# n|credit.creditBureau.creditData[0].creditCollateral|0
# c|credit.creditBureau.creditData[0].creditCurrency|rur
# d|credit.creditBureau.creditData[0].creditDate|29.12.2011 00:00:00
# n|credit.creditBureau.creditData[0].creditDayOverdue|0
# d|credit.creditBureau.creditData[0].creditEndDate|02.04.2012 00:00:00
# d|credit.creditBureau.creditData[0].creditEndDateFact|02.04.2012 00:00:00
# n|credit.creditBureau.creditData[0].creditJoint|0
# n|credit.creditBureau.creditData[0].creditMaxOverdue|0
# c|credit.creditBureau.creditData[0].creditOwner|0
# n|credit.creditBureau.creditData[0].creditProlong|0
# n|credit.creditBureau.creditData[0].creditSum|3640
# n|credit.creditBureau.creditData[0].creditSumDebt|0
# n|credit.creditBureau.creditData[0].creditSumLimit|0
# n|credit.creditBureau.creditData[0].creditSumOverdue|0
# n|credit.creditBureau.creditData[0].creditSumType|1
# n|credit.creditBureau.creditData[0].creditType|5
# c|credit.creditBureau.creditData[0].creditTypeUni|5
# d|credit.creditBureau.creditData[0].creditUpdate|31.07.2012 00:00:00
# n|credit.creditBureau.creditData[0].cuid|60268391
# n|credit.creditBureau.creditData[0].delay30|0
# n|credit.creditBureau.creditData[0].delay5|0
# n|credit.creditBureau.creditData[0].delay60|0
# n|credit.creditBureau.creditData[0].delay90|0
# n|credit.creditBureau.creditData[0].delayMore|0
# c|credit.creditBureau.creditData[1].cbId|equ
# c|credit.creditBureau.creditData[1].contractSource|cb
# n|credit.creditBureau.creditData[1].cred_ratio|0
# n|credit.creditBureau.creditData[1].creditActive|0
# n|credit.creditBureau.creditData[1].creditCollateral|0
# c|credit.creditBureau.creditData[1].creditCurrency|rur
# d|credit.creditBureau.creditData[1].creditDate|29.12.2011 00:00:00
# n|credit.creditBureau.creditData[1].creditDayOverdue|0
# d|credit.creditBureau.creditData[1].creditEndDate|02.04.2012 00:00:00
# d|credit.creditBureau.creditData[1].creditEndDateFact|02.04.2012 00:00:00
# n|credit.creditBureau.creditData[1].creditJoint|0
# n|credit.creditBureau.creditData[1].creditMaxOverdue|0
# c|credit.creditBureau.creditData[1].creditOwner|0
# n|credit.creditBureau.creditData[1].creditProlong|0
# n|credit.creditBureau.creditData[1].creditSum|3640
# n|credit.creditBureau.creditData[1].creditSumDebt|0
# n|credit.creditBureau.creditData[1].creditSumLimit|0
# n|credit.creditBureau.creditData[1].creditSumOverdue|0
# n|credit.creditBureau.creditData[1].creditSumType|1
# n|credit.creditBureau.creditData[1].creditType|5
# c|credit.creditBureau.creditData[1].creditTypeUni|5
# d|credit.creditBureau.creditData[1].creditUpdate|05.04.2012 00:00:00
# n|credit.creditBureau.creditData[1].cuid|60268391
# n|credit.creditBureau.creditData[1].delay30|0
# n|credit.creditBureau.creditData[1].delay5|0
# n|credit.creditBureau.creditData[1].delay60|0
# n|credit.creditBureau.creditData[1].delay90|0
# n|credit.creditBureau.creditData[1].delayMore|0
# n|credit.creditBureau.creditData[2].cbAnnuity|2168
# c|credit.creditBureau.creditData[2].cbId|exp
# c|credit.creditBureau.creditData[2].cbOverdueLine|-000000000100000100
# c|credit.creditBureau.creditData[2].contractSource|cb
# n|credit.creditBureau.creditData[2].cred_ratio|0
# n|credit.creditBureau.creditData[2].creditActive|1
# n|credit.creditBureau.creditData[2].creditCollateral|0
# n|credit.creditBureau.creditData[2].creditCostRate|19.9
# c|credit.creditBureau.creditData[2].creditCurrency|rur
# d|credit.creditBureau.creditData[2].creditDate|17.10.2018 00:00:00
# n|credit.creditBureau.creditData[2].creditDayOverdue|30
# d|credit.creditBureau.creditData[2].creditEndDate|17.10.2020 00:00:00
# n|credit.creditBureau.creditData[2].creditJoint|0
# n|credit.creditBureau.creditData[2].creditMaxOverdue|2173
# c|credit.creditBureau.creditData[2].creditOwner|0
# n|credit.creditBureau.creditData[2].creditProlong|0
# n|credit.creditBureau.creditData[2].creditSum|42635
# n|credit.creditBureau.creditData[2].creditSumDebt|16498
# n|credit.creditBureau.creditData[2].creditSumLimit|0
# n|credit.creditBureau.creditData[2].creditSumOverdue|2173
# n|credit.creditBureau.creditData[2].creditSumType|1
# n|credit.creditBureau.creditData[2].creditType|5
# c|credit.creditBureau.creditData[2].creditTypeUni|5
# d|credit.creditBureau.creditData[2].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[2].cuid|60268391
# n|credit.creditBureau.creditData[2].delay30|0
# n|credit.creditBureau.creditData[2].delay5|2
# n|credit.creditBureau.creditData[2].delay60|0
# n|credit.creditBureau.creditData[2].delay90|0
# n|credit.creditBureau.creditData[2].delayMore|0
# n|credit.creditBureau.creditData[3].cbAnnuity|1137
# c|credit.creditBureau.creditData[3].cbId|exp
# c|credit.creditBureau.creditData[3].cbOverdueLine|-000000000000000000010000000000
# c|credit.creditBureau.creditData[3].contractSource|cb
# n|credit.creditBureau.creditData[3].cred_ratio|0
# n|credit.creditBureau.creditData[3].creditActive|1
# n|credit.creditBureau.creditData[3].creditCollateral|0
# n|credit.creditBureau.creditData[3].creditCostRate|19.9
# c|credit.creditBureau.creditData[3].creditCurrency|rur
# d|credit.creditBureau.creditData[3].creditDate|24.10.2017 00:00:00
# n|credit.creditBureau.creditData[3].creditDayOverdue|30
# d|credit.creditBureau.creditData[3].creditEndDate|24.10.2022 00:00:00
# n|credit.creditBureau.creditData[3].creditJoint|0
# n|credit.creditBureau.creditData[3].creditMaxOverdue|1141
# c|credit.creditBureau.creditData[3].creditOwner|0
# n|credit.creditBureau.creditData[3].creditProlong|0
# n|credit.creditBureau.creditData[3].creditSum|43000
# n|credit.creditBureau.creditData[3].creditSumDebt|28756
# n|credit.creditBureau.creditData[3].creditSumLimit|0
# n|credit.creditBureau.creditData[3].creditSumOverdue|1139
# n|credit.creditBureau.creditData[3].creditSumType|1
# n|credit.creditBureau.creditData[3].creditType|5
# c|credit.creditBureau.creditData[3].creditTypeUni|5
# d|credit.creditBureau.creditData[3].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[3].cuid|60268391
# n|credit.creditBureau.creditData[3].delay30|0
# n|credit.creditBureau.creditData[3].delay5|1
# n|credit.creditBureau.creditData[3].delay60|0
# n|credit.creditBureau.creditData[3].delay90|0
# n|credit.creditBureau.creditData[3].delayMore|0
# c|credit.creditBureau.creditData[4].cbId|exp
# c|credit.creditBureau.creditData[4].cbOverdueLine|10110011000011000001111000000000000000000000000000000-0-----
# c|credit.creditBureau.creditData[4].contractSource|cb
# n|credit.creditBureau.creditData[4].cred_ratio|0
# n|credit.creditBureau.creditData[4].creditActive|1
# n|credit.creditBureau.creditData[4].creditCollateral|0
# n|credit.creditBureau.creditData[4].creditCostRate|26.03
# c|credit.creditBureau.creditData[4].creditCurrency|rur
# d|credit.creditBureau.creditData[4].creditDate|07.05.2015 00:00:00
# n|credit.creditBureau.creditData[4].creditDayOverdue|30
# n|credit.creditBureau.creditData[4].creditJoint|0
# n|credit.creditBureau.creditData[4].creditMaxOverdue|1824
# c|credit.creditBureau.creditData[4].creditOwner|0
# n|credit.creditBureau.creditData[4].creditProlong|0
# n|credit.creditBureau.creditData[4].creditSum|30000
# n|credit.creditBureau.creditData[4].creditSumDebt|31254
# n|credit.creditBureau.creditData[4].creditSumLimit|0
# n|credit.creditBureau.creditData[4].creditSumOverdue|1824
# n|credit.creditBureau.creditData[4].creditSumType|1
# n|credit.creditBureau.creditData[4].creditType|4
# c|credit.creditBureau.creditData[4].creditTypeUni|4
# d|credit.creditBureau.creditData[4].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[4].cuid|60268391
# n|credit.creditBureau.creditData[4].delay30|0
# n|credit.creditBureau.creditData[4].delay5|10
# n|credit.creditBureau.creditData[4].delay60|0
# n|credit.creditBureau.creditData[4].delay90|0
# n|credit.creditBureau.creditData[4].delayMore|0
# c|credit.creditBureau.creditData[5].cbId|equ
# c|credit.creditBureau.creditData[5].contractSource|cb
# n|credit.creditBureau.creditData[5].cred_ratio|0
# n|credit.creditBureau.creditData[5].creditActive|0
# n|credit.creditBureau.creditData[5].creditCollateral|0
# c|credit.creditBureau.creditData[5].creditCurrency|rur
# d|credit.creditBureau.creditData[5].creditDate|15.05.2009 00:00:00
# n|credit.creditBureau.creditData[5].creditDayOverdue|0
# d|credit.creditBureau.creditData[5].creditEndDate|16.11.2009 00:00:00
# d|credit.creditBureau.creditData[5].creditEndDateFact|17.08.2009 00:00:00
# n|credit.creditBureau.creditData[5].creditJoint|0
# n|credit.creditBureau.creditData[5].creditMaxOverdue|0
# c|credit.creditBureau.creditData[5].creditOwner|0
# n|credit.creditBureau.creditData[5].creditProlong|0
# n|credit.creditBureau.creditData[5].creditSum|12990
# n|credit.creditBureau.creditData[5].creditSumDebt|0
# n|credit.creditBureau.creditData[5].creditSumLimit|0
# n|credit.creditBureau.creditData[5].creditSumOverdue|0
# n|credit.creditBureau.creditData[5].creditSumType|1
# n|credit.creditBureau.creditData[5].creditType|5
# c|credit.creditBureau.creditData[5].creditTypeUni|5
# d|credit.creditBureau.creditData[5].creditUpdate|17.08.2009 00:00:00
# n|credit.creditBureau.creditData[5].cuid|60268391
# n|credit.creditBureau.creditData[5].delay30|0
# n|credit.creditBureau.creditData[5].delay5|0
# n|credit.creditBureau.creditData[5].delay60|0
# n|credit.creditBureau.creditData[5].delay90|0
# n|credit.creditBureau.creditData[5].delayMore|0
# n|credit.creditBureau.creditData[6].cbAnnuity|0
# c|credit.creditBureau.creditData[6].cbId|nbk
# c|credit.creditBureau.creditData[6].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC0000--
# c|credit.creditBureau.creditData[6].contractSource|cb
# n|credit.creditBureau.creditData[6].cred_ratio|0
# n|credit.creditBureau.creditData[6].creditActive|0
# n|credit.creditBureau.creditData[6].creditCollateral|0
# c|credit.creditBureau.creditData[6].creditCurrency|rur
# d|credit.creditBureau.creditData[6].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[6].creditDayOverdue|0
# d|credit.creditBureau.creditData[6].creditEndDate|03.04.2013 00:00:00
# d|credit.creditBureau.creditData[6].creditEndDateFact|03.04.2013 00:00:00
# n|credit.creditBureau.creditData[6].creditJoint|0
# n|credit.creditBureau.creditData[6].creditMaxOverdue|0
# c|credit.creditBureau.creditData[6].creditOwner|0
# n|credit.creditBureau.creditData[6].creditProlong|0
# n|credit.creditBureau.creditData[6].creditSum|11912
# n|credit.creditBureau.creditData[6].creditSumDebt|0
# n|credit.creditBureau.creditData[6].creditSumLimit|0
# n|credit.creditBureau.creditData[6].creditSumOverdue|0
# n|credit.creditBureau.creditData[6].creditSumType|1
# n|credit.creditBureau.creditData[6].creditType|5
# c|credit.creditBureau.creditData[6].creditTypeUni|5
# d|credit.creditBureau.creditData[6].creditUpdate|06.04.2013 00:00:00
# n|credit.creditBureau.creditData[6].cuid|60268391
# n|credit.creditBureau.creditData[6].delay30|0
# n|credit.creditBureau.creditData[6].delay5|0
# n|credit.creditBureau.creditData[6].delay60|0
# n|credit.creditBureau.creditData[6].delay90|0
# n|credit.creditBureau.creditData[6].delayMore|0
# n|credit.creditBureau.creditData[7].cbAnnuity|0
# c|credit.creditBureau.creditData[7].cbId|nbk
# c|credit.creditBureau.creditData[7].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC0-0000000000-
# c|credit.creditBureau.creditData[7].contractSource|cb
# n|credit.creditBureau.creditData[7].cred_ratio|0
# n|credit.creditBureau.creditData[7].creditActive|0
# n|credit.creditBureau.creditData[7].creditCollateral|0
# n|credit.creditBureau.creditData[7].creditCostRate|31.122
# c|credit.creditBureau.creditData[7].creditCurrency|rur
# d|credit.creditBureau.creditData[7].creditDate|14.07.2015 00:00:00
# n|credit.creditBureau.creditData[7].creditDayOverdue|0
# d|credit.creditBureau.creditData[7].creditEndDate|14.07.2016 00:00:00
# d|credit.creditBureau.creditData[7].creditEndDateFact|16.08.2016 00:00:00
# n|credit.creditBureau.creditData[7].creditJoint|0
# n|credit.creditBureau.creditData[7].creditMaxOverdue|0
# c|credit.creditBureau.creditData[7].creditOwner|0
# n|credit.creditBureau.creditData[7].creditProlong|0
# n|credit.creditBureau.creditData[7].creditSum|15010
# n|credit.creditBureau.creditData[7].creditSumDebt|0
# n|credit.creditBureau.creditData[7].creditSumLimit|0
# n|credit.creditBureau.creditData[7].creditSumOverdue|0
# n|credit.creditBureau.creditData[7].creditSumType|1
# n|credit.creditBureau.creditData[7].creditType|5
# c|credit.creditBureau.creditData[7].creditTypeUni|5
# d|credit.creditBureau.creditData[7].creditUpdate|16.08.2016 00:00:00
# n|credit.creditBureau.creditData[7].cuid|60268391
# n|credit.creditBureau.creditData[7].delay30|0
# n|credit.creditBureau.creditData[7].delay5|0
# n|credit.creditBureau.creditData[7].delay60|0
# n|credit.creditBureau.creditData[7].delay90|0
# n|credit.creditBureau.creditData[7].delayMore|0
# n|credit.creditBureau.creditData[8].cbAnnuity|0
# c|credit.creditBureau.creditData[8].cbId|nbk
# c|credit.creditBureau.creditData[8].contractSource|cb
# n|credit.creditBureau.creditData[8].cred_ratio|0
# n|credit.creditBureau.creditData[8].creditActive|1
# n|credit.creditBureau.creditData[8].creditCollateral|0
# n|credit.creditBureau.creditData[8].creditCostRate|28.75
# c|credit.creditBureau.creditData[8].creditCurrency|rur
# d|credit.creditBureau.creditData[8].creditDate|20.04.2020 00:00:00
# n|credit.creditBureau.creditData[8].creditDayOverdue|0
# d|credit.creditBureau.creditData[8].creditEndDate|28.02.2025 00:00:00
# n|credit.creditBureau.creditData[8].creditJoint|0
# n|credit.creditBureau.creditData[8].creditMaxOverdue|0
# c|credit.creditBureau.creditData[8].creditOwner|0
# n|credit.creditBureau.creditData[8].creditProlong|0
# n|credit.creditBureau.creditData[8].creditSum|5000
# n|credit.creditBureau.creditData[8].creditSumDebt|4953
# n|credit.creditBureau.creditData[8].creditSumLimit|47
# n|credit.creditBureau.creditData[8].creditSumOverdue|0
# n|credit.creditBureau.creditData[8].creditSumType|1
# n|credit.creditBureau.creditData[8].creditType|4
# c|credit.creditBureau.creditData[8].creditTypeUni|4
# d|credit.creditBureau.creditData[8].creditUpdate|03.05.2020 00:00:00
# n|credit.creditBureau.creditData[8].cuid|60268391
# n|credit.creditBureau.creditData[8].delay30|0
# n|credit.creditBureau.creditData[8].delay5|0
# n|credit.creditBureau.creditData[8].delay60|0
# n|credit.creditBureau.creditData[8].delay90|0
# n|credit.creditBureau.creditData[8].delayMore|0
# n|credit.creditBureau.creditData[9].cbAnnuity|4488
# c|credit.creditBureau.creditData[9].cbId|nbk
# c|credit.creditBureau.creditData[9].cbOverdueLine|0000000000020000000-
# c|credit.creditBureau.creditData[9].contractSource|cb
# n|credit.creditBureau.creditData[9].cred_ratio|0
# n|credit.creditBureau.creditData[9].creditActive|1
# n|credit.creditBureau.creditData[9].creditCollateral|0
# n|credit.creditBureau.creditData[9].creditCostRate|22.9
# c|credit.creditBureau.creditData[9].creditCurrency|rur
# d|credit.creditBureau.creditData[9].creditDate|14.09.2018 00:00:00
# n|credit.creditBureau.creditData[9].creditDayOverdue|0
# d|credit.creditBureau.creditData[9].creditEndDate|16.12.2021 00:00:00
# n|credit.creditBureau.creditData[9].creditJoint|0
# n|credit.creditBureau.creditData[9].creditMaxOverdue|0
# c|credit.creditBureau.creditData[9].creditOwner|0
# n|credit.creditBureau.creditData[9].creditProlong|0
# n|credit.creditBureau.creditData[9].creditSum|58224
# n|credit.creditBureau.creditData[9].creditSumDebt|38747
# n|credit.creditBureau.creditData[9].creditSumLimit|0
# n|credit.creditBureau.creditData[9].creditSumOverdue|0
# n|credit.creditBureau.creditData[9].creditSumType|1
# n|credit.creditBureau.creditData[9].creditType|5
# c|credit.creditBureau.creditData[9].creditTypeUni|5
# d|credit.creditBureau.creditData[9].creditUpdate|09.05.2020 00:00:00
# n|credit.creditBureau.creditData[9].cuid|60268391
# n|credit.creditBureau.creditData[9].delay30|1
# n|credit.creditBureau.creditData[9].delay5|0
# n|credit.creditBureau.creditData[9].delay60|0
# n|credit.creditBureau.creditData[9].delay90|0
# n|credit.creditBureau.creditData[9].delayMore|0
# n|credit.creditBureau.creditData[10].cbAnnuity|3018
# c|credit.creditBureau.creditData[10].cbId|exp
# c|credit.creditBureau.creditData[10].cbOverdueLine|-00000000000
# c|credit.creditBureau.creditData[10].contractSource|cb
# n|credit.creditBureau.creditData[10].cred_ratio|0
# n|credit.creditBureau.creditData[10].creditActive|1
# n|credit.creditBureau.creditData[10].creditCollateral|0
# n|credit.creditBureau.creditData[10].creditCostRate|19.94
# c|credit.creditBureau.creditData[10].creditCurrency|rur
# d|credit.creditBureau.creditData[10].creditDate|13.05.2019 00:00:00
# n|credit.creditBureau.creditData[10].creditDayOverdue|30
# d|credit.creditBureau.creditData[10].creditEndDate|13.03.2022 00:00:00
# n|credit.creditBureau.creditData[10].creditJoint|0
# n|credit.creditBureau.creditData[10].creditMaxOverdue|3025
# c|credit.creditBureau.creditData[10].creditOwner|0
# n|credit.creditBureau.creditData[10].creditProlong|0
# n|credit.creditBureau.creditData[10].creditSum|77951
# n|credit.creditBureau.creditData[10].creditSumDebt|60929
# n|credit.creditBureau.creditData[10].creditSumLimit|0
# n|credit.creditBureau.creditData[10].creditSumOverdue|3025
# n|credit.creditBureau.creditData[10].creditSumType|1
# n|credit.creditBureau.creditData[10].creditType|5
# c|credit.creditBureau.creditData[10].creditTypeUni|5
# d|credit.creditBureau.creditData[10].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[10].cuid|60268391
# n|credit.creditBureau.creditData[10].delay30|0
# n|credit.creditBureau.creditData[10].delay5|0
# n|credit.creditBureau.creditData[10].delay60|0
# n|credit.creditBureau.creditData[10].delay90|0
# n|credit.creditBureau.creditData[10].delayMore|0
# c|credit.creditBureau.creditData[11].cbId|equ
# c|credit.creditBureau.creditData[11].contractSource|cb
# n|credit.creditBureau.creditData[11].cred_ratio|0
# n|credit.creditBureau.creditData[11].creditActive|1
# n|credit.creditBureau.creditData[11].creditCollateral|0
# n|credit.creditBureau.creditData[11].creditCostRate|28.75
# c|credit.creditBureau.creditData[11].creditCurrency|rur
# d|credit.creditBureau.creditData[11].creditDate|20.04.2020 00:00:00
# n|credit.creditBureau.creditData[11].creditDayOverdue|0
# d|credit.creditBureau.creditData[11].creditEndDate|28.02.2025 00:00:00
# n|credit.creditBureau.creditData[11].creditJoint|0
# n|credit.creditBureau.creditData[11].creditMaxOverdue|0
# c|credit.creditBureau.creditData[11].creditOwner|0
# n|credit.creditBureau.creditData[11].creditProlong|0
# n|credit.creditBureau.creditData[11].creditSum|5000
# n|credit.creditBureau.creditData[11].creditSumDebt|4953.29
# n|credit.creditBureau.creditData[11].creditSumLimit|46.71
# n|credit.creditBureau.creditData[11].creditSumOverdue|0
# n|credit.creditBureau.creditData[11].creditSumType|1
# n|credit.creditBureau.creditData[11].creditType|4
# c|credit.creditBureau.creditData[11].creditTypeUni|4
# d|credit.creditBureau.creditData[11].creditUpdate|03.05.2020 00:00:00
# n|credit.creditBureau.creditData[11].cuid|60268391
# n|credit.creditBureau.creditData[11].delay30|0
# n|credit.creditBureau.creditData[11].delay5|0
# n|credit.creditBureau.creditData[11].delay60|0
# n|credit.creditBureau.creditData[11].delay90|0
# n|credit.creditBureau.creditData[11].delayMore|0
# n|credit.creditBureau.creditData[12].cbAnnuity|0
# c|credit.creditBureau.creditData[12].cbId|exp
# c|credit.creditBureau.creditData[12].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC00000000000000000
# c|credit.creditBureau.creditData[12].contractSource|cb
# n|credit.creditBureau.creditData[12].cred_ratio|0
# n|credit.creditBureau.creditData[12].creditActive|0
# n|credit.creditBureau.creditData[12].creditCollateral|0
# n|credit.creditBureau.creditData[12].creditCostRate|22.02
# c|credit.creditBureau.creditData[12].creditCurrency|rur
# d|credit.creditBureau.creditData[12].creditDate|03.05.2016 00:00:00
# n|credit.creditBureau.creditData[12].creditDayOverdue|0
# d|credit.creditBureau.creditData[12].creditEndDate|03.05.2018 00:00:00
# d|credit.creditBureau.creditData[12].creditEndDateFact|24.10.2017 00:00:00
# n|credit.creditBureau.creditData[12].creditJoint|0
# n|credit.creditBureau.creditData[12].creditMaxOverdue|0
# c|credit.creditBureau.creditData[12].creditOwner|0
# n|credit.creditBureau.creditData[12].creditProlong|0
# n|credit.creditBureau.creditData[12].creditSum|37717
# n|credit.creditBureau.creditData[12].creditSumDebt|0
# n|credit.creditBureau.creditData[12].creditSumLimit|0
# n|credit.creditBureau.creditData[12].creditSumOverdue|0
# n|credit.creditBureau.creditData[12].creditSumType|1
# n|credit.creditBureau.creditData[12].creditType|5
# c|credit.creditBureau.creditData[12].creditTypeUni|5
# d|credit.creditBureau.creditData[12].creditUpdate|15.05.2019 00:00:00
# n|credit.creditBureau.creditData[12].cuid|60268391
# n|credit.creditBureau.creditData[12].delay30|0
# n|credit.creditBureau.creditData[12].delay5|0
# n|credit.creditBureau.creditData[12].delay60|0
# n|credit.creditBureau.creditData[12].delay90|0
# n|credit.creditBureau.creditData[12].delayMore|0
# n|credit.creditBureau.creditData[13].cbAnnuity|0
# c|credit.creditBureau.creditData[13].cbId|exp
# c|credit.creditBureau.creditData[13].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC111111111110101011101000
# c|credit.creditBureau.creditData[13].contractSource|cb
# n|credit.creditBureau.creditData[13].cred_ratio|0
# n|credit.creditBureau.creditData[13].creditActive|0
# n|credit.creditBureau.creditData[13].creditCollateral|0
# n|credit.creditBureau.creditData[13].creditCostRate|24.57
# c|credit.creditBureau.creditData[13].creditCurrency|rur
# d|credit.creditBureau.creditData[13].creditDate|07.05.2015 00:00:00
# n|credit.creditBureau.creditData[13].creditDayOverdue|0
# d|credit.creditBureau.creditData[13].creditEndDate|07.05.2017 00:00:00
# d|credit.creditBureau.creditData[13].creditEndDateFact|13.05.2017 00:00:00
# n|credit.creditBureau.creditData[13].creditJoint|0
# n|credit.creditBureau.creditData[13].creditMaxOverdue|5651
# c|credit.creditBureau.creditData[13].creditOwner|0
# n|credit.creditBureau.creditData[13].creditProlong|0
# n|credit.creditBureau.creditData[13].creditSum|106400
# n|credit.creditBureau.creditData[13].creditSumDebt|0
# n|credit.creditBureau.creditData[13].creditSumLimit|0
# n|credit.creditBureau.creditData[13].creditSumOverdue|0
# n|credit.creditBureau.creditData[13].creditSumType|1
# n|credit.creditBureau.creditData[13].creditType|5
# c|credit.creditBureau.creditData[13].creditTypeUni|5
# d|credit.creditBureau.creditData[13].creditUpdate|15.05.2019 00:00:00
# n|credit.creditBureau.creditData[13].cuid|60268391
# n|credit.creditBureau.creditData[13].delay30|0
# n|credit.creditBureau.creditData[13].delay5|17
# n|credit.creditBureau.creditData[13].delay60|0
# n|credit.creditBureau.creditData[13].delay90|0
# n|credit.creditBureau.creditData[13].delayMore|0
# c|credit.creditBureau.creditData[14].cbId|equ
# c|credit.creditBureau.creditData[14].contractSource|cb
# n|credit.creditBureau.creditData[14].cred_ratio|0
# n|credit.creditBureau.creditData[14].creditActive|0
# n|credit.creditBureau.creditData[14].creditCollateral|0
# n|credit.creditBureau.creditData[14].creditCostRate|39.96
# c|credit.creditBureau.creditData[14].creditCurrency|rur
# d|credit.creditBureau.creditData[14].creditDate|28.10.2014 00:00:00
# n|credit.creditBureau.creditData[14].creditDayOverdue|0
# d|credit.creditBureau.creditData[14].creditEndDate|28.04.2015 00:00:00
# d|credit.creditBureau.creditData[14].creditEndDateFact|29.04.2015 00:00:00
# n|credit.creditBureau.creditData[14].creditJoint|0
# n|credit.creditBureau.creditData[14].creditMaxOverdue|0
# c|credit.creditBureau.creditData[14].creditOwner|0
# n|credit.creditBureau.creditData[14].creditProlong|0
# n|credit.creditBureau.creditData[14].creditSum|4390
# n|credit.creditBureau.creditData[14].creditSumDebt|0
# n|credit.creditBureau.creditData[14].creditSumLimit|0
# n|credit.creditBureau.creditData[14].creditSumOverdue|0
# n|credit.creditBureau.creditData[14].creditSumType|1
# n|credit.creditBureau.creditData[14].creditType|5
# c|credit.creditBureau.creditData[14].creditTypeUni|5
# d|credit.creditBureau.creditData[14].creditUpdate|29.04.2015 00:00:00
# n|credit.creditBureau.creditData[14].cuid|60268391
# n|credit.creditBureau.creditData[14].delay30|0
# n|credit.creditBureau.creditData[14].delay5|0
# n|credit.creditBureau.creditData[14].delay60|0
# n|credit.creditBureau.creditData[14].delay90|0
# n|credit.creditBureau.creditData[14].delayMore|0
# c|credit.creditBureau.creditData[15].cbId|equ
# c|credit.creditBureau.creditData[15].contractSource|cb
# n|credit.creditBureau.creditData[15].cred_ratio|0
# n|credit.creditBureau.creditData[15].creditActive|0
# n|credit.creditBureau.creditData[15].creditCollateral|0
# c|credit.creditBureau.creditData[15].creditCurrency|rur
# d|credit.creditBureau.creditData[15].creditDate|15.02.2014 00:00:00
# n|credit.creditBureau.creditData[15].creditDayOverdue|0
# d|credit.creditBureau.creditData[15].creditEndDate|16.02.2015 00:00:00
# d|credit.creditBureau.creditData[15].creditEndDateFact|15.01.2015 00:00:00
# n|credit.creditBureau.creditData[15].creditJoint|0
# n|credit.creditBureau.creditData[15].creditMaxOverdue|0
# c|credit.creditBureau.creditData[15].creditOwner|0
# n|credit.creditBureau.creditData[15].creditProlong|0
# n|credit.creditBureau.creditData[15].creditSum|15950
# n|credit.creditBureau.creditData[15].creditSumDebt|0
# n|credit.creditBureau.creditData[15].creditSumLimit|0
# n|credit.creditBureau.creditData[15].creditSumOverdue|0
# n|credit.creditBureau.creditData[15].creditSumType|1
# n|credit.creditBureau.creditData[15].creditType|5
# c|credit.creditBureau.creditData[15].creditTypeUni|5
# d|credit.creditBureau.creditData[15].creditUpdate|15.01.2015 00:00:00
# n|credit.creditBureau.creditData[15].cuid|60268391
# n|credit.creditBureau.creditData[15].delay30|0
# n|credit.creditBureau.creditData[15].delay5|0
# n|credit.creditBureau.creditData[15].delay60|0
# n|credit.creditBureau.creditData[15].delay90|0
# n|credit.creditBureau.creditData[15].delayMore|0
# c|credit.creditBureau.creditData[16].cbId|equ
# c|credit.creditBureau.creditData[16].contractSource|cb
# n|credit.creditBureau.creditData[16].cred_ratio|0
# n|credit.creditBureau.creditData[16].creditActive|0
# n|credit.creditBureau.creditData[16].creditCollateral|0
# n|credit.creditBureau.creditData[16].creditCostRate|51.1
# c|credit.creditBureau.creditData[16].creditCurrency|rur
# d|credit.creditBureau.creditData[16].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[16].creditDayOverdue|0
# d|credit.creditBureau.creditData[16].creditEndDate|31.12.2099 00:00:00
# d|credit.creditBureau.creditData[16].creditEndDateFact|15.03.2018 00:00:00
# n|credit.creditBureau.creditData[16].creditJoint|0
# n|credit.creditBureau.creditData[16].creditMaxOverdue|0
# c|credit.creditBureau.creditData[16].creditOwner|0
# n|credit.creditBureau.creditData[16].creditProlong|0
# n|credit.creditBureau.creditData[16].creditSum|0
# n|credit.creditBureau.creditData[16].creditSumDebt|0
# n|credit.creditBureau.creditData[16].creditSumLimit|0
# n|credit.creditBureau.creditData[16].creditSumOverdue|0
# n|credit.creditBureau.creditData[16].creditSumType|1
# n|credit.creditBureau.creditData[16].creditType|4
# c|credit.creditBureau.creditData[16].creditTypeUni|4
# d|credit.creditBureau.creditData[16].creditUpdate|15.03.2018 00:00:00
# n|credit.creditBureau.creditData[16].cuid|60268391
# n|credit.creditBureau.creditData[16].delay30|0
# n|credit.creditBureau.creditData[16].delay5|0
# n|credit.creditBureau.creditData[16].delay60|0
# n|credit.creditBureau.creditData[16].delay90|0
# n|credit.creditBureau.creditData[16].delayMore|0
# n|credit.creditBureau.creditData[17].cbAnnuity|0
# c|credit.creditBureau.creditData[17].cbId|nbk
# c|credit.creditBureau.creditData[17].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC-0--
# c|credit.creditBureau.creditData[17].contractSource|cb
# n|credit.creditBureau.creditData[17].cred_ratio|0
# n|credit.creditBureau.creditData[17].creditActive|0
# n|credit.creditBureau.creditData[17].creditCollateral|0
# c|credit.creditBureau.creditData[17].creditCurrency|rur
# d|credit.creditBureau.creditData[17].creditDate|29.12.2011 00:00:00
# n|credit.creditBureau.creditData[17].creditDayOverdue|0
# d|credit.creditBureau.creditData[17].creditEndDate|02.04.2012 00:00:00
# d|credit.creditBureau.creditData[17].creditEndDateFact|02.04.2012 00:00:00
# n|credit.creditBureau.creditData[17].creditJoint|0
# n|credit.creditBureau.creditData[17].creditMaxOverdue|0
# c|credit.creditBureau.creditData[17].creditOwner|0
# n|credit.creditBureau.creditData[17].creditProlong|0
# n|credit.creditBureau.creditData[17].creditSum|3640
# n|credit.creditBureau.creditData[17].creditSumDebt|0
# n|credit.creditBureau.creditData[17].creditSumLimit|0
# n|credit.creditBureau.creditData[17].creditSumOverdue|0
# n|credit.creditBureau.creditData[17].creditSumType|1
# n|credit.creditBureau.creditData[17].creditType|5
# c|credit.creditBureau.creditData[17].creditTypeUni|5
# d|credit.creditBureau.creditData[17].creditUpdate|05.04.2012 00:00:00
# n|credit.creditBureau.creditData[17].cuid|60268391
# n|credit.creditBureau.creditData[17].delay30|0
# n|credit.creditBureau.creditData[17].delay5|0
# n|credit.creditBureau.creditData[17].delay60|0
# n|credit.creditBureau.creditData[17].delay90|0
# n|credit.creditBureau.creditData[17].delayMore|0
# c|credit.creditBureau.creditData[18].cbId|equ
# c|credit.creditBureau.creditData[18].contractSource|cb
# n|credit.creditBureau.creditData[18].cred_ratio|0
# n|credit.creditBureau.creditData[18].creditActive|0
# n|credit.creditBureau.creditData[18].creditCollateral|0
# n|credit.creditBureau.creditData[18].creditCostRate|36.49
# c|credit.creditBureau.creditData[18].creditCurrency|rur
# d|credit.creditBureau.creditData[18].creditDate|12.12.2016 00:00:00
# n|credit.creditBureau.creditData[18].creditDayOverdue|0
# d|credit.creditBureau.creditData[18].creditEndDate|12.02.2018 00:00:00
# d|credit.creditBureau.creditData[18].creditEndDateFact|13.11.2017 00:00:00
# n|credit.creditBureau.creditData[18].creditJoint|0
# n|credit.creditBureau.creditData[18].creditMaxOverdue|0
# c|credit.creditBureau.creditData[18].creditOwner|0
# n|credit.creditBureau.creditData[18].creditProlong|0
# n|credit.creditBureau.creditData[18].creditSum|18289
# n|credit.creditBureau.creditData[18].creditSumDebt|0
# n|credit.creditBureau.creditData[18].creditSumLimit|0
# n|credit.creditBureau.creditData[18].creditSumOverdue|0
# n|credit.creditBureau.creditData[18].creditSumType|1
# n|credit.creditBureau.creditData[18].creditType|5
# c|credit.creditBureau.creditData[18].creditTypeUni|5
# d|credit.creditBureau.creditData[18].creditUpdate|13.11.2017 00:00:00
# n|credit.creditBureau.creditData[18].cuid|60268391
# n|credit.creditBureau.creditData[18].delay30|0
# n|credit.creditBureau.creditData[18].delay5|0
# n|credit.creditBureau.creditData[18].delay60|0
# n|credit.creditBureau.creditData[18].delay90|0
# n|credit.creditBureau.creditData[18].delayMore|0
# c|credit.creditBureau.creditData[19].cbId|equ
# c|credit.creditBureau.creditData[19].contractSource|cb
# n|credit.creditBureau.creditData[19].cred_ratio|0
# n|credit.creditBureau.creditData[19].creditActive|1
# n|credit.creditBureau.creditData[19].creditCollateral|0
# n|credit.creditBureau.creditData[19].creditCostRate|22.9
# c|credit.creditBureau.creditData[19].creditCurrency|rur
# d|credit.creditBureau.creditData[19].creditDate|14.09.2018 00:00:00
# n|credit.creditBureau.creditData[19].creditDayOverdue|0
# d|credit.creditBureau.creditData[19].creditEndDate|16.12.2021 00:00:00
# n|credit.creditBureau.creditData[19].creditJoint|0
# n|credit.creditBureau.creditData[19].creditMaxOverdue|1541.24
# c|credit.creditBureau.creditData[19].creditOwner|0
# n|credit.creditBureau.creditData[19].creditProlong|3
# n|credit.creditBureau.creditData[19].creditSum|58224
# n|credit.creditBureau.creditData[19].creditSumDebt|37685.46
# n|credit.creditBureau.creditData[19].creditSumLimit|0
# n|credit.creditBureau.creditData[19].creditSumOverdue|0
# n|credit.creditBureau.creditData[19].creditSumType|1
# n|credit.creditBureau.creditData[19].creditType|5
# c|credit.creditBureau.creditData[19].creditTypeUni|5
# d|credit.creditBureau.creditData[19].creditUpdate|16.04.2020 00:00:00
# n|credit.creditBureau.creditData[19].cuid|60268391
# n|credit.creditBureau.creditData[19].delay30|0
# n|credit.creditBureau.creditData[19].delay5|7
# n|credit.creditBureau.creditData[19].delay60|0
# n|credit.creditBureau.creditData[19].delay90|0
# n|credit.creditBureau.creditData[19].delayMore|0
# n|credit.creditBureau.creditData[20].cbAnnuity|0
# c|credit.creditBureau.creditData[20].cbId|exp
# c|credit.creditBureau.creditData[20].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC0000000001000
# c|credit.creditBureau.creditData[20].contractSource|cb
# n|credit.creditBureau.creditData[20].cred_ratio|0
# n|credit.creditBureau.creditData[20].creditActive|0
# n|credit.creditBureau.creditData[20].creditCollateral|0
# n|credit.creditBureau.creditData[20].creditCostRate|31.122
# c|credit.creditBureau.creditData[20].creditCurrency|rur
# d|credit.creditBureau.creditData[20].creditDate|14.07.2015 00:00:00
# n|credit.creditBureau.creditData[20].creditDayOverdue|0
# d|credit.creditBureau.creditData[20].creditEndDate|14.07.2016 00:00:00
# d|credit.creditBureau.creditData[20].creditEndDateFact|16.08.2016 00:00:00
# n|credit.creditBureau.creditData[20].creditJoint|0
# n|credit.creditBureau.creditData[20].creditMaxOverdue|1740
# c|credit.creditBureau.creditData[20].creditOwner|0
# n|credit.creditBureau.creditData[20].creditProlong|0
# n|credit.creditBureau.creditData[20].creditSum|15010
# n|credit.creditBureau.creditData[20].creditSumDebt|0
# n|credit.creditBureau.creditData[20].creditSumLimit|0
# n|credit.creditBureau.creditData[20].creditSumOverdue|0
# n|credit.creditBureau.creditData[20].creditSumType|1
# n|credit.creditBureau.creditData[20].creditType|5
# c|credit.creditBureau.creditData[20].creditTypeUni|5
# d|credit.creditBureau.creditData[20].creditUpdate|22.08.2016 00:00:00
# n|credit.creditBureau.creditData[20].cuid|60268391
# n|credit.creditBureau.creditData[20].delay30|0
# n|credit.creditBureau.creditData[20].delay5|1
# n|credit.creditBureau.creditData[20].delay60|0
# n|credit.creditBureau.creditData[20].delay90|0
# n|credit.creditBureau.creditData[20].delayMore|0
# n|credit.creditBureau.creditData[21].cbAnnuity|0
# c|credit.creditBureau.creditData[21].cbId|exp
# c|credit.creditBureau.creditData[21].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC00000000000
# c|credit.creditBureau.creditData[21].contractSource|cb
# n|credit.creditBureau.creditData[21].cred_ratio|0
# n|credit.creditBureau.creditData[21].creditActive|0
# n|credit.creditBureau.creditData[21].creditCollateral|0
# n|credit.creditBureau.creditData[21].creditCostRate|36.49
# c|credit.creditBureau.creditData[21].creditCurrency|rur
# d|credit.creditBureau.creditData[21].creditDate|12.12.2016 00:00:00
# n|credit.creditBureau.creditData[21].creditDayOverdue|0
# d|credit.creditBureau.creditData[21].creditEndDate|12.02.2018 00:00:00
# d|credit.creditBureau.creditData[21].creditEndDateFact|13.11.2017 00:00:00
# n|credit.creditBureau.creditData[21].creditJoint|0
# n|credit.creditBureau.creditData[21].creditMaxOverdue|0
# c|credit.creditBureau.creditData[21].creditOwner|0
# n|credit.creditBureau.creditData[21].creditProlong|0
# n|credit.creditBureau.creditData[21].creditSum|18289
# n|credit.creditBureau.creditData[21].creditSumDebt|0
# n|credit.creditBureau.creditData[21].creditSumLimit|0
# n|credit.creditBureau.creditData[21].creditSumOverdue|0
# n|credit.creditBureau.creditData[21].creditSumType|1
# n|credit.creditBureau.creditData[21].creditType|5
# c|credit.creditBureau.creditData[21].creditTypeUni|5
# d|credit.creditBureau.creditData[21].creditUpdate|14.11.2017 00:00:00
# n|credit.creditBureau.creditData[21].cuid|60268391
# n|credit.creditBureau.creditData[21].delay30|0
# n|credit.creditBureau.creditData[21].delay5|0
# n|credit.creditBureau.creditData[21].delay60|0
# n|credit.creditBureau.creditData[21].delay90|0
# n|credit.creditBureau.creditData[21].delayMore|0
# n|credit.creditBureau.creditData[22].cbAnnuity|0
# c|credit.creditBureau.creditData[22].cbId|exp
# c|credit.creditBureau.creditData[22].cbOverdueLine|CCCCCCCCCCCC000000001000000000000000
# c|credit.creditBureau.creditData[22].contractSource|cb
# n|credit.creditBureau.creditData[22].cred_ratio|0
# n|credit.creditBureau.creditData[22].creditActive|0
# n|credit.creditBureau.creditData[22].creditCollateral|0
# n|credit.creditBureau.creditData[22].creditCostRate|18.94
# c|credit.creditBureau.creditData[22].creditCurrency|rur
# d|credit.creditBureau.creditData[22].creditDate|29.05.2017 00:00:00
# n|credit.creditBureau.creditData[22].creditDayOverdue|0
# d|credit.creditBureau.creditData[22].creditEndDate|29.05.2019 00:00:00
# d|credit.creditBureau.creditData[22].creditEndDateFact|30.05.2019 00:00:00
# n|credit.creditBureau.creditData[22].creditJoint|0
# n|credit.creditBureau.creditData[22].creditMaxOverdue|5389
# c|credit.creditBureau.creditData[22].creditOwner|0
# n|credit.creditBureau.creditData[22].creditProlong|0
# n|credit.creditBureau.creditData[22].creditSum|106600
# n|credit.creditBureau.creditData[22].creditSumDebt|0
# n|credit.creditBureau.creditData[22].creditSumLimit|0
# n|credit.creditBureau.creditData[22].creditSumOverdue|0
# n|credit.creditBureau.creditData[22].creditSumType|1
# n|credit.creditBureau.creditData[22].creditType|5
# c|credit.creditBureau.creditData[22].creditTypeUni|5
# d|credit.creditBureau.creditData[22].creditUpdate|02.06.2019 00:00:00
# n|credit.creditBureau.creditData[22].cuid|60268391
# n|credit.creditBureau.creditData[22].delay30|0
# n|credit.creditBureau.creditData[22].delay5|1
# n|credit.creditBureau.creditData[22].delay60|0
# n|credit.creditBureau.creditData[22].delay90|0
# n|credit.creditBureau.creditData[22].delayMore|0
# n|credit.creditBureau.creditData[23].cbAnnuity|0
# c|credit.creditBureau.creditData[23].cbId|exp
# c|credit.creditBureau.creditData[23].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC-00000
# c|credit.creditBureau.creditData[23].contractSource|cb
# n|credit.creditBureau.creditData[23].cred_ratio|0
# n|credit.creditBureau.creditData[23].creditActive|0
# n|credit.creditBureau.creditData[23].creditCollateral|0
# c|credit.creditBureau.creditData[23].creditCurrency|rur
# d|credit.creditBureau.creditData[23].creditDate|28.10.2014 00:00:00
# n|credit.creditBureau.creditData[23].creditDayOverdue|0
# d|credit.creditBureau.creditData[23].creditEndDate|28.04.2015 00:00:00
# d|credit.creditBureau.creditData[23].creditEndDateFact|29.04.2015 00:00:00
# n|credit.creditBureau.creditData[23].creditJoint|0
# n|credit.creditBureau.creditData[23].creditMaxOverdue|0
# c|credit.creditBureau.creditData[23].creditOwner|0
# n|credit.creditBureau.creditData[23].creditProlong|0
# n|credit.creditBureau.creditData[23].creditSum|4390
# n|credit.creditBureau.creditData[23].creditSumDebt|0
# n|credit.creditBureau.creditData[23].creditSumLimit|0
# n|credit.creditBureau.creditData[23].creditSumOverdue|0
# n|credit.creditBureau.creditData[23].creditSumType|1
# n|credit.creditBureau.creditData[23].creditType|5
# c|credit.creditBureau.creditData[23].creditTypeUni|5
# d|credit.creditBureau.creditData[23].creditUpdate|30.05.2015 00:00:00
# n|credit.creditBureau.creditData[23].cuid|60268391
# n|credit.creditBureau.creditData[23].delay30|0
# n|credit.creditBureau.creditData[23].delay5|0
# n|credit.creditBureau.creditData[23].delay60|0
# n|credit.creditBureau.creditData[23].delay90|0
# n|credit.creditBureau.creditData[23].delayMore|0
# n|credit.creditBureau.creditData[24].cbAnnuity|2219
# c|credit.creditBureau.creditData[24].cbId|exp
# c|credit.creditBureau.creditData[24].cbOverdueLine|0000110100001000000110
# c|credit.creditBureau.creditData[24].contractSource|cb
# n|credit.creditBureau.creditData[24].cred_ratio|0
# n|credit.creditBureau.creditData[24].creditActive|1
# n|credit.creditBureau.creditData[24].creditCollateral|0
# n|credit.creditBureau.creditData[24].creditCostRate|19.9
# c|credit.creditBureau.creditData[24].creditCurrency|rur
# d|credit.creditBureau.creditData[24].creditDate|11.07.2018 00:00:00
# n|credit.creditBureau.creditData[24].creditDayOverdue|30
# d|credit.creditBureau.creditData[24].creditEndDate|11.07.2020 00:00:00
# n|credit.creditBureau.creditData[24].creditJoint|0
# n|credit.creditBureau.creditData[24].creditMaxOverdue|2220
# c|credit.creditBureau.creditData[24].creditOwner|0
# n|credit.creditBureau.creditData[24].creditProlong|0
# n|credit.creditBureau.creditData[24].creditSum|43500
# n|credit.creditBureau.creditData[24].creditSumDebt|7868
# n|credit.creditBureau.creditData[24].creditSumLimit|0
# n|credit.creditBureau.creditData[24].creditSumOverdue|1373
# n|credit.creditBureau.creditData[24].creditSumType|1
# n|credit.creditBureau.creditData[24].creditType|5
# c|credit.creditBureau.creditData[24].creditTypeUni|5
# d|credit.creditBureau.creditData[24].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[24].cuid|60268391
# n|credit.creditBureau.creditData[24].delay30|0
# n|credit.creditBureau.creditData[24].delay5|6
# n|credit.creditBureau.creditData[24].delay60|0
# n|credit.creditBureau.creditData[24].delay90|0
# n|credit.creditBureau.creditData[24].delayMore|0
# n|credit.creditBureau.creditData[25].cbAnnuity|0
# c|credit.creditBureau.creditData[25].cbId|nbk
# c|credit.creditBureau.creditData[25].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCC--0------0000000000000000000000000000-0000000000---000-0000000000
# c|credit.creditBureau.creditData[25].contractSource|cb
# n|credit.creditBureau.creditData[25].cred_ratio|0
# n|credit.creditBureau.creditData[25].creditActive|0
# n|credit.creditBureau.creditData[25].creditCollateral|0
# n|credit.creditBureau.creditData[25].creditCostRate|51.1
# c|credit.creditBureau.creditData[25].creditCurrency|rur
# d|credit.creditBureau.creditData[25].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[25].creditDayOverdue|0
# d|credit.creditBureau.creditData[25].creditEndDate|31.12.2099 00:00:00
# d|credit.creditBureau.creditData[25].creditEndDateFact|15.03.2018 00:00:00
# n|credit.creditBureau.creditData[25].creditJoint|0
# n|credit.creditBureau.creditData[25].creditMaxOverdue|0
# c|credit.creditBureau.creditData[25].creditOwner|0
# n|credit.creditBureau.creditData[25].creditProlong|0
# n|credit.creditBureau.creditData[25].creditSum|0
# n|credit.creditBureau.creditData[25].creditSumDebt|0
# n|credit.creditBureau.creditData[25].creditSumLimit|0
# n|credit.creditBureau.creditData[25].creditSumOverdue|0
# n|credit.creditBureau.creditData[25].creditSumType|1
# n|credit.creditBureau.creditData[25].creditType|4
# c|credit.creditBureau.creditData[25].creditTypeUni|4
# d|credit.creditBureau.creditData[25].creditUpdate|15.03.2018 00:00:00
# n|credit.creditBureau.creditData[25].cuid|60268391
# n|credit.creditBureau.creditData[25].delay30|0
# n|credit.creditBureau.creditData[25].delay5|0
# n|credit.creditBureau.creditData[25].delay60|0
# n|credit.creditBureau.creditData[25].delay90|0
# n|credit.creditBureau.creditData[25].delayMore|0
# n|credit.creditBureau.creditData[26].cbAnnuity|0
# c|credit.creditBureau.creditData[26].cbId|exp
# c|credit.creditBureau.creditData[26].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCC--0------000000-0000-0000000000000000-0000000000---00000000000000
# c|credit.creditBureau.creditData[26].contractSource|cb
# n|credit.creditBureau.creditData[26].cred_ratio|0
# n|credit.creditBureau.creditData[26].creditActive|0
# n|credit.creditBureau.creditData[26].creditCollateral|0
# n|credit.creditBureau.creditData[26].creditCostRate|51.1
# c|credit.creditBureau.creditData[26].creditCurrency|rur
# d|credit.creditBureau.creditData[26].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[26].creditDayOverdue|0
# d|credit.creditBureau.creditData[26].creditEndDate|31.12.2099 00:00:00
# d|credit.creditBureau.creditData[26].creditEndDateFact|15.03.2018 00:00:00
# n|credit.creditBureau.creditData[26].creditJoint|0
# n|credit.creditBureau.creditData[26].creditMaxOverdue|0
# c|credit.creditBureau.creditData[26].creditOwner|0
# n|credit.creditBureau.creditData[26].creditProlong|0
# n|credit.creditBureau.creditData[26].creditSum|0
# n|credit.creditBureau.creditData[26].creditSumDebt|0
# n|credit.creditBureau.creditData[26].creditSumLimit|0
# n|credit.creditBureau.creditData[26].creditSumOverdue|0
# n|credit.creditBureau.creditData[26].creditSumType|1
# n|credit.creditBureau.creditData[26].creditType|4
# c|credit.creditBureau.creditData[26].creditTypeUni|4
# d|credit.creditBureau.creditData[26].creditUpdate|16.03.2018 00:00:00
# n|credit.creditBureau.creditData[26].cuid|60268391
# n|credit.creditBureau.creditData[26].delay30|0
# n|credit.creditBureau.creditData[26].delay5|0
# n|credit.creditBureau.creditData[26].delay60|0
# n|credit.creditBureau.creditData[26].delay90|0
# n|credit.creditBureau.creditData[26].delayMore|0
# n|credit.creditBureau.creditData[27].cbAnnuity|0
# c|credit.creditBureau.creditData[27].cbId|exp
# c|credit.creditBureau.creditData[27].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC000000
# c|credit.creditBureau.creditData[27].contractSource|cb
# n|credit.creditBureau.creditData[27].cred_ratio|0
# n|credit.creditBureau.creditData[27].creditActive|0
# n|credit.creditBureau.creditData[27].creditCollateral|0
# c|credit.creditBureau.creditData[27].creditCurrency|rur
# d|credit.creditBureau.creditData[27].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[27].creditDayOverdue|0
# d|credit.creditBureau.creditData[27].creditEndDate|03.04.2013 00:00:00
# d|credit.creditBureau.creditData[27].creditEndDateFact|03.04.2013 00:00:00
# n|credit.creditBureau.creditData[27].creditJoint|0
# n|credit.creditBureau.creditData[27].creditMaxOverdue|0
# c|credit.creditBureau.creditData[27].creditOwner|0
# n|credit.creditBureau.creditData[27].creditProlong|0
# n|credit.creditBureau.creditData[27].creditSum|11912
# n|credit.creditBureau.creditData[27].creditSumDebt|0
# n|credit.creditBureau.creditData[27].creditSumLimit|0
# n|credit.creditBureau.creditData[27].creditSumOverdue|0
# n|credit.creditBureau.creditData[27].creditSumType|1
# n|credit.creditBureau.creditData[27].creditType|5
# c|credit.creditBureau.creditData[27].creditTypeUni|5
# d|credit.creditBureau.creditData[27].creditUpdate|10.04.2013 00:00:00
# n|credit.creditBureau.creditData[27].cuid|60268391
# n|credit.creditBureau.creditData[27].delay30|0
# n|credit.creditBureau.creditData[27].delay5|0
# n|credit.creditBureau.creditData[27].delay60|0
# n|credit.creditBureau.creditData[27].delay90|0
# n|credit.creditBureau.creditData[27].delayMore|0
# n|credit.creditBureau.creditData[28].cbAnnuity|0
# c|credit.creditBureau.creditData[28].cbId|nbk
# c|credit.creditBureau.creditData[28].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC000-00
# c|credit.creditBureau.creditData[28].contractSource|cb
# n|credit.creditBureau.creditData[28].cred_ratio|0
# n|credit.creditBureau.creditData[28].creditActive|0
# n|credit.creditBureau.creditData[28].creditCollateral|0
# n|credit.creditBureau.creditData[28].creditCostRate|39.96
# c|credit.creditBureau.creditData[28].creditCurrency|rur
# d|credit.creditBureau.creditData[28].creditDate|28.10.2014 00:00:00
# n|credit.creditBureau.creditData[28].creditDayOverdue|0
# d|credit.creditBureau.creditData[28].creditEndDate|28.04.2015 00:00:00
# d|credit.creditBureau.creditData[28].creditEndDateFact|29.04.2015 00:00:00
# n|credit.creditBureau.creditData[28].creditJoint|0
# n|credit.creditBureau.creditData[28].creditMaxOverdue|0
# c|credit.creditBureau.creditData[28].creditOwner|0
# n|credit.creditBureau.creditData[28].creditProlong|0
# n|credit.creditBureau.creditData[28].creditSum|4390
# n|credit.creditBureau.creditData[28].creditSumDebt|0
# n|credit.creditBureau.creditData[28].creditSumLimit|0
# n|credit.creditBureau.creditData[28].creditSumOverdue|0
# n|credit.creditBureau.creditData[28].creditSumType|1
# n|credit.creditBureau.creditData[28].creditType|5
# c|credit.creditBureau.creditData[28].creditTypeUni|5
# d|credit.creditBureau.creditData[28].creditUpdate|29.04.2015 00:00:00
# n|credit.creditBureau.creditData[28].cuid|60268391
# n|credit.creditBureau.creditData[28].delay30|0
# n|credit.creditBureau.creditData[28].delay5|0
# n|credit.creditBureau.creditData[28].delay60|0
# n|credit.creditBureau.creditData[28].delay90|0
# n|credit.creditBureau.creditData[28].delayMore|0
# n|credit.creditBureau.creditData[29].cbAnnuity|0
# c|credit.creditBureau.creditData[29].cbId|nbk
# c|credit.creditBureau.creditData[29].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC00-
# c|credit.creditBureau.creditData[29].contractSource|cb
# n|credit.creditBureau.creditData[29].cred_ratio|0
# n|credit.creditBureau.creditData[29].creditActive|0
# n|credit.creditBureau.creditData[29].creditCollateral|0
# c|credit.creditBureau.creditData[29].creditCurrency|rur
# d|credit.creditBureau.creditData[29].creditDate|15.05.2009 00:00:00
# n|credit.creditBureau.creditData[29].creditDayOverdue|0
# d|credit.creditBureau.creditData[29].creditEndDate|16.11.2009 00:00:00
# d|credit.creditBureau.creditData[29].creditEndDateFact|17.08.2009 00:00:00
# n|credit.creditBureau.creditData[29].creditJoint|0
# n|credit.creditBureau.creditData[29].creditMaxOverdue|0
# c|credit.creditBureau.creditData[29].creditOwner|0
# n|credit.creditBureau.creditData[29].creditProlong|0
# n|credit.creditBureau.creditData[29].creditSum|12990
# n|credit.creditBureau.creditData[29].creditSumDebt|0
# n|credit.creditBureau.creditData[29].creditSumLimit|0
# n|credit.creditBureau.creditData[29].creditSumOverdue|0
# n|credit.creditBureau.creditData[29].creditSumType|1
# n|credit.creditBureau.creditData[29].creditType|5
# c|credit.creditBureau.creditData[29].creditTypeUni|5
# d|credit.creditBureau.creditData[29].creditUpdate|17.08.2009 00:00:00
# n|credit.creditBureau.creditData[29].cuid|60268391
# n|credit.creditBureau.creditData[29].delay30|0
# n|credit.creditBureau.creditData[29].delay5|0
# n|credit.creditBureau.creditData[29].delay60|0
# n|credit.creditBureau.creditData[29].delay90|0
# n|credit.creditBureau.creditData[29].delayMore|0
# c|credit.creditBureau.creditData[30].cbId|equ
# c|credit.creditBureau.creditData[30].contractSource|cb
# n|credit.creditBureau.creditData[30].cred_ratio|0
# n|credit.creditBureau.creditData[30].creditActive|0
# n|credit.creditBureau.creditData[30].creditCollateral|0
# c|credit.creditBureau.creditData[30].creditCurrency|rur
# d|credit.creditBureau.creditData[30].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[30].creditDayOverdue|0
# d|credit.creditBureau.creditData[30].creditEndDate|03.04.2013 00:00:00
# d|credit.creditBureau.creditData[30].creditEndDateFact|03.04.2013 00:00:00
# n|credit.creditBureau.creditData[30].creditJoint|0
# n|credit.creditBureau.creditData[30].creditMaxOverdue|0
# c|credit.creditBureau.creditData[30].creditOwner|0
# n|credit.creditBureau.creditData[30].creditProlong|0
# n|credit.creditBureau.creditData[30].creditSum|11911.92
# n|credit.creditBureau.creditData[30].creditSumDebt|0
# n|credit.creditBureau.creditData[30].creditSumLimit|0
# n|credit.creditBureau.creditData[30].creditSumOverdue|0
# n|credit.creditBureau.creditData[30].creditSumType|1
# n|credit.creditBureau.creditData[30].creditType|5
# c|credit.creditBureau.creditData[30].creditTypeUni|5
# d|credit.creditBureau.creditData[30].creditUpdate|06.04.2013 00:00:00
# n|credit.creditBureau.creditData[30].cuid|60268391
# n|credit.creditBureau.creditData[30].delay30|0
# n|credit.creditBureau.creditData[30].delay5|0
# n|credit.creditBureau.creditData[30].delay60|0
# n|credit.creditBureau.creditData[30].delay90|0
# n|credit.creditBureau.creditData[30].delayMore|0
# c|credit.creditBureau.creditData[31].cbId|equ
# c|credit.creditBureau.creditData[31].contractSource|cb
# n|credit.creditBureau.creditData[31].cred_ratio|0
# n|credit.creditBureau.creditData[31].creditActive|0
# n|credit.creditBureau.creditData[31].creditCollateral|0
# n|credit.creditBureau.creditData[31].creditCostRate|31.122
# c|credit.creditBureau.creditData[31].creditCurrency|rur
# d|credit.creditBureau.creditData[31].creditDate|14.07.2015 00:00:00
# n|credit.creditBureau.creditData[31].creditDayOverdue|0
# d|credit.creditBureau.creditData[31].creditEndDate|14.07.2016 00:00:00
# d|credit.creditBureau.creditData[31].creditEndDateFact|16.08.2016 00:00:00
# n|credit.creditBureau.creditData[31].creditJoint|0
# n|credit.creditBureau.creditData[31].creditMaxOverdue|1146.12
# c|credit.creditBureau.creditData[31].creditOwner|0
# n|credit.creditBureau.creditData[31].creditProlong|0
# n|credit.creditBureau.creditData[31].creditSum|15010
# n|credit.creditBureau.creditData[31].creditSumDebt|0
# n|credit.creditBureau.creditData[31].creditSumLimit|0
# n|credit.creditBureau.creditData[31].creditSumOverdue|0
# n|credit.creditBureau.creditData[31].creditSumType|1
# n|credit.creditBureau.creditData[31].creditType|5
# c|credit.creditBureau.creditData[31].creditTypeUni|5
# d|credit.creditBureau.creditData[31].creditUpdate|16.08.2016 00:00:00
# n|credit.creditBureau.creditData[31].cuid|60268391
# n|credit.creditBureau.creditData[31].delay30|1
# n|credit.creditBureau.creditData[31].delay5|0
# n|credit.creditBureau.creditData[31].delay60|0
# n|credit.creditBureau.creditData[31].delay90|0
# n|credit.creditBureau.creditData[31].delayMore|0
# n|credit.creditBureau.creditData[32].cbAnnuity|1128
# c|credit.creditBureau.creditData[32].cbId|exp
# c|credit.creditBureau.creditData[32].cbOverdueLine|-001100000000000100010000
# c|credit.creditBureau.creditData[32].contractSource|cb
# n|credit.creditBureau.creditData[32].cred_ratio|0
# n|credit.creditBureau.creditData[32].creditActive|1
# n|credit.creditBureau.creditData[32].creditCollateral|0
# n|credit.creditBureau.creditData[32].creditCostRate|17.36
# c|credit.creditBureau.creditData[32].creditCurrency|rur
# d|credit.creditBureau.creditData[32].creditDate|05.04.2018 00:00:00
# n|credit.creditBureau.creditData[32].creditDayOverdue|30
# d|credit.creditBureau.creditData[32].creditEndDate|05.04.2021 00:00:00
# n|credit.creditBureau.creditData[32].creditJoint|0
# n|credit.creditBureau.creditData[32].creditMaxOverdue|1131
# c|credit.creditBureau.creditData[32].creditOwner|0
# n|credit.creditBureau.creditData[32].creditProlong|0
# n|credit.creditBureau.creditData[32].creditSum|31490
# n|credit.creditBureau.creditData[32].creditSumDebt|13577
# n|credit.creditBureau.creditData[32].creditSumLimit|0
# n|credit.creditBureau.creditData[32].creditSumOverdue|1131
# n|credit.creditBureau.creditData[32].creditSumType|1
# n|credit.creditBureau.creditData[32].creditType|5
# c|credit.creditBureau.creditData[32].creditTypeUni|5
# d|credit.creditBureau.creditData[32].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[32].cuid|60268391
# n|credit.creditBureau.creditData[32].delay30|0
# n|credit.creditBureau.creditData[32].delay5|4
# n|credit.creditBureau.creditData[32].delay60|0
# n|credit.creditBureau.creditData[32].delay90|0
# n|credit.creditBureau.creditData[32].delayMore|0
# n|credit.creditBureau.creditData[33].cbAnnuity|0
# c|credit.creditBureau.creditData[33].cbId|exp
# c|credit.creditBureau.creditData[33].cbOverdueLine|0
# c|credit.creditBureau.creditData[33].contractSource|cb
# n|credit.creditBureau.creditData[33].cred_ratio|0
# n|credit.creditBureau.creditData[33].creditActive|1
# n|credit.creditBureau.creditData[33].creditCollateral|0
# n|credit.creditBureau.creditData[33].creditCostRate|28.75
# c|credit.creditBureau.creditData[33].creditCurrency|rur
# d|credit.creditBureau.creditData[33].creditDate|20.04.2020 00:00:00
# n|credit.creditBureau.creditData[33].creditDayOverdue|0
# d|credit.creditBureau.creditData[33].creditEndDate|28.02.2025 00:00:00
# n|credit.creditBureau.creditData[33].creditJoint|0
# n|credit.creditBureau.creditData[33].creditMaxOverdue|0
# c|credit.creditBureau.creditData[33].creditOwner|0
# n|credit.creditBureau.creditData[33].creditProlong|0
# n|credit.creditBureau.creditData[33].creditSum|5000
# n|credit.creditBureau.creditData[33].creditSumDebt|4953
# n|credit.creditBureau.creditData[33].creditSumLimit|47
# n|credit.creditBureau.creditData[33].creditSumOverdue|0
# n|credit.creditBureau.creditData[33].creditSumType|1
# n|credit.creditBureau.creditData[33].creditType|4
# c|credit.creditBureau.creditData[33].creditTypeUni|4
# d|credit.creditBureau.creditData[33].creditUpdate|05.05.2020 00:00:00
# n|credit.creditBureau.creditData[33].cuid|60268391
# n|credit.creditBureau.creditData[33].delay30|0
# n|credit.creditBureau.creditData[33].delay5|0
# n|credit.creditBureau.creditData[33].delay60|0
# n|credit.creditBureau.creditData[33].delay90|0
# n|credit.creditBureau.creditData[33].delayMore|0
# n|credit.creditBureau.creditData[34].cbAnnuity|4488
# c|credit.creditBureau.creditData[34].cbId|exp
# c|credit.creditBureau.creditData[34].cbOverdueLine|01000001000011011000
# c|credit.creditBureau.creditData[34].contractSource|cb
# n|credit.creditBureau.creditData[34].cred_ratio|0
# n|credit.creditBureau.creditData[34].creditActive|1
# n|credit.creditBureau.creditData[34].creditCollateral|0
# n|credit.creditBureau.creditData[34].creditCostRate|22.9
# c|credit.creditBureau.creditData[34].creditCurrency|rur
# d|credit.creditBureau.creditData[34].creditDate|14.09.2018 00:00:00
# n|credit.creditBureau.creditData[34].creditDayOverdue|0
# d|credit.creditBureau.creditData[34].creditEndDate|16.12.2021 00:00:00
# n|credit.creditBureau.creditData[34].creditJoint|0
# n|credit.creditBureau.creditData[34].creditMaxOverdue|3287
# c|credit.creditBureau.creditData[34].creditOwner|0
# n|credit.creditBureau.creditData[34].creditProlong|0
# n|credit.creditBureau.creditData[34].creditSum|58224
# n|credit.creditBureau.creditData[34].creditSumDebt|38747
# n|credit.creditBureau.creditData[34].creditSumLimit|0
# n|credit.creditBureau.creditData[34].creditSumOverdue|0
# n|credit.creditBureau.creditData[34].creditSumType|1
# n|credit.creditBureau.creditData[34].creditType|5
# c|credit.creditBureau.creditData[34].creditTypeUni|5
# d|credit.creditBureau.creditData[34].creditUpdate|07.05.2020 00:00:00
# n|credit.creditBureau.creditData[34].cuid|60268391
# n|credit.creditBureau.creditData[34].delay30|0
# n|credit.creditBureau.creditData[34].delay5|6
# n|credit.creditBureau.creditData[34].delay60|0
# n|credit.creditBureau.creditData[34].delay90|0
# n|credit.creditBureau.creditData[34].delayMore|0
# n|credit.creditBureau.creditData[35].cbAnnuity|0
# c|credit.creditBureau.creditData[35].cbId|exp
# c|credit.creditBureau.creditData[35].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC00000000000
# c|credit.creditBureau.creditData[35].contractSource|cb
# n|credit.creditBureau.creditData[35].cred_ratio|0
# n|credit.creditBureau.creditData[35].creditActive|0
# n|credit.creditBureau.creditData[35].creditCollateral|0
# c|credit.creditBureau.creditData[35].creditCurrency|rur
# d|credit.creditBureau.creditData[35].creditDate|15.03.2020 00:00:00
# n|credit.creditBureau.creditData[35].creditDayOverdue|0
# n|credit.creditBureau.creditData[35].creditJoint|1
# n|credit.creditBureau.creditData[35].creditMaxOverdue|0
# n|credit.creditBureau.creditData[35].creditProlong|0
# n|credit.creditBureau.creditData[35].creditSum|50000
# n|credit.creditBureau.creditData[35].creditSumLimit|0
# n|credit.creditBureau.creditData[35].creditSumOverdue|0
# n|credit.creditBureau.creditData[35].creditSumType|1
# n|credit.creditBureau.creditData[35].creditType|5
# c|credit.creditBureau.creditData[35].creditTypeUni|5
# d|credit.creditBureau.creditData[35].creditUpdate|15.01.2015 00:00:00
# n|credit.creditBureau.creditData[35].cuid|60268391
# n|credit.creditBureau.creditData[35].delay30|0
# n|credit.creditBureau.creditData[35].delay5|0
# n|credit.creditBureau.creditData[35].delay60|0
# n|credit.creditBureau.creditData[35].delay90|0
# n|credit.creditBureau.creditData[35].delayMore|0
# n|credit.creditBureau.creditData[36].cbAnnuity|0
# c|credit.creditBureau.creditData[36].contractSource|cb
# n|credit.creditBureau.creditData[36].cred_ratio|0
# n|credit.creditBureau.creditData[36].creditActive|0
# n|credit.creditBureau.creditData[36].creditCollateral|0
# c|credit.creditBureau.creditData[36].creditCurrency|rur
# d|credit.creditBureau.creditData[36].creditDate|15.02.2014 00:00:00
# n|credit.creditBureau.creditData[36].creditDayOverdue|0
# d|credit.creditBureau.creditData[36].creditEndDate|16.02.2015 00:00:00
# d|credit.creditBureau.creditData[36].creditEndDateFact|15.01.2015 00:00:00
# n|credit.creditBureau.creditData[36].creditJoint|1
# n|credit.creditBureau.creditData[36].creditMaxOverdue|0
# c|credit.creditBureau.creditData[36].creditOwner|0
# n|credit.creditBureau.creditData[36].creditProlong|0
# n|credit.creditBureau.creditData[36].creditSum|15950
# n|credit.creditBureau.creditData[36].creditSumDebt|0
# n|credit.creditBureau.creditData[36].creditSumLimit|0
# n|credit.creditBureau.creditData[36].creditSumOverdue|0
# n|credit.creditBureau.creditData[36].creditSumType|1
# n|credit.creditBureau.creditData[36].creditType|5
# c|credit.creditBureau.creditData[36].creditTypeUni|5
# d|credit.creditBureau.creditData[36].creditUpdate|15.01.2015 00:00:00
# n|credit.creditBureau.creditData[36].cuid|60268391
# n|credit.creditBureau.creditData[36].delay30|0
# n|credit.creditBureau.creditData[36].delay5|0
# n|credit.creditBureau.creditData[36].delay60|0
# n|credit.creditBureau.creditData[36].delay90|0
# n|credit.creditBureau.creditData[36].delayMore|0
# n|credit.creditBureau.creditData[37].cbAnnuity|2219
# c|credit.creditBureau.creditData[37].cbOverdueLine|0000110100001000000110
# c|credit.creditBureau.creditData[37].contractSource|cb
# n|credit.creditBureau.creditData[37].cred_ratio|0
# n|credit.creditBureau.creditData[37].creditActive|1
# n|credit.creditBureau.creditData[37].creditCollateral|0
# n|credit.creditBureau.creditData[37].creditCostRate|19.9
# c|credit.creditBureau.creditData[37].creditCurrency|rur
# d|credit.creditBureau.creditData[37].creditDate|11.07.2018 00:00:00
# n|credit.creditBureau.creditData[37].creditDayOverdue|30
# d|credit.creditBureau.creditData[37].creditEndDate|11.07.2020 00:00:00
# n|credit.creditBureau.creditData[37].creditJoint|1
# n|credit.creditBureau.creditData[37].creditMaxOverdue|2220
# c|credit.creditBureau.creditData[37].creditOwner|0
# n|credit.creditBureau.creditData[37].creditProlong|0
# n|credit.creditBureau.creditData[37].creditSum|43500
# n|credit.creditBureau.creditData[37].creditSumDebt|7868
# n|credit.creditBureau.creditData[37].creditSumLimit|0
# n|credit.creditBureau.creditData[37].creditSumOverdue|1373
# n|credit.creditBureau.creditData[37].creditSumType|1
# n|credit.creditBureau.creditData[37].creditType|5
# c|credit.creditBureau.creditData[37].creditTypeUni|5
# d|credit.creditBureau.creditData[37].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[37].cuid|60268391
# n|credit.creditBureau.creditData[37].delay30|0
# n|credit.creditBureau.creditData[37].delay5|6
# n|credit.creditBureau.creditData[37].delay60|0
# n|credit.creditBureau.creditData[37].delay90|0
# n|credit.creditBureau.creditData[37].delayMore|0
# c|credit.creditBureau.creditData[38].cbOverdueLine|10110011000011000001111000000000000000000000000000000-0-----
# c|credit.creditBureau.creditData[38].contractSource|cb
# n|credit.creditBureau.creditData[38].cred_ratio|0
# n|credit.creditBureau.creditData[38].creditActive|1
# n|credit.creditBureau.creditData[38].creditCollateral|0
# n|credit.creditBureau.creditData[38].creditCostRate|26.03
# c|credit.creditBureau.creditData[38].creditCurrency|rur
# d|credit.creditBureau.creditData[38].creditDate|07.05.2015 00:00:00
# n|credit.creditBureau.creditData[38].creditDayOverdue|30
# n|credit.creditBureau.creditData[38].creditJoint|1
# n|credit.creditBureau.creditData[38].creditMaxOverdue|1824
# c|credit.creditBureau.creditData[38].creditOwner|0
# n|credit.creditBureau.creditData[38].creditProlong|0
# n|credit.creditBureau.creditData[38].creditSum|30000
# n|credit.creditBureau.creditData[38].creditSumDebt|31254
# n|credit.creditBureau.creditData[38].creditSumLimit|0
# n|credit.creditBureau.creditData[38].creditSumOverdue|1824
# n|credit.creditBureau.creditData[38].creditSumType|1
# n|credit.creditBureau.creditData[38].creditType|4
# c|credit.creditBureau.creditData[38].creditTypeUni|4
# d|credit.creditBureau.creditData[38].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[38].cuid|60268391
# n|credit.creditBureau.creditData[38].delay30|0
# n|credit.creditBureau.creditData[38].delay5|10
# n|credit.creditBureau.creditData[38].delay60|0
# n|credit.creditBureau.creditData[38].delay90|0
# n|credit.creditBureau.creditData[38].delayMore|0
# n|credit.creditBureau.creditData[39].cbAnnuity|0
# c|credit.creditBureau.creditData[39].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC-00000
# c|credit.creditBureau.creditData[39].contractSource|cb
# n|credit.creditBureau.creditData[39].cred_ratio|0
# n|credit.creditBureau.creditData[39].creditActive|0
# n|credit.creditBureau.creditData[39].creditCollateral|0
# c|credit.creditBureau.creditData[39].creditCurrency|rur
# d|credit.creditBureau.creditData[39].creditDate|28.10.2014 00:00:00
# n|credit.creditBureau.creditData[39].creditDayOverdue|0
# d|credit.creditBureau.creditData[39].creditEndDate|28.04.2015 00:00:00
# d|credit.creditBureau.creditData[39].creditEndDateFact|29.04.2015 00:00:00
# n|credit.creditBureau.creditData[39].creditJoint|1
# n|credit.creditBureau.creditData[39].creditMaxOverdue|0
# c|credit.creditBureau.creditData[39].creditOwner|0
# n|credit.creditBureau.creditData[39].creditProlong|0
# n|credit.creditBureau.creditData[39].creditSum|4390
# n|credit.creditBureau.creditData[39].creditSumDebt|0
# n|credit.creditBureau.creditData[39].creditSumLimit|0
# n|credit.creditBureau.creditData[39].creditSumOverdue|0
# n|credit.creditBureau.creditData[39].creditSumType|1
# n|credit.creditBureau.creditData[39].creditType|5
# c|credit.creditBureau.creditData[39].creditTypeUni|5
# d|credit.creditBureau.creditData[39].creditUpdate|30.05.2015 00:00:00
# n|credit.creditBureau.creditData[39].cuid|60268391
# n|credit.creditBureau.creditData[39].delay30|0
# n|credit.creditBureau.creditData[39].delay5|0
# n|credit.creditBureau.creditData[39].delay60|0
# n|credit.creditBureau.creditData[39].delay90|0
# n|credit.creditBureau.creditData[39].delayMore|0
# n|credit.creditBureau.creditData[40].cbAnnuity|0
# c|credit.creditBureau.creditData[40].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC0000000001000
# c|credit.creditBureau.creditData[40].contractSource|cb
# n|credit.creditBureau.creditData[40].cred_ratio|0
# n|credit.creditBureau.creditData[40].creditActive|0
# n|credit.creditBureau.creditData[40].creditCollateral|0
# n|credit.creditBureau.creditData[40].creditCostRate|31.122
# c|credit.creditBureau.creditData[40].creditCurrency|rur
# d|credit.creditBureau.creditData[40].creditDate|14.07.2015 00:00:00
# n|credit.creditBureau.creditData[40].creditDayOverdue|0
# d|credit.creditBureau.creditData[40].creditEndDate|14.07.2016 00:00:00
# d|credit.creditBureau.creditData[40].creditEndDateFact|16.08.2016 00:00:00
# n|credit.creditBureau.creditData[40].creditJoint|1
# n|credit.creditBureau.creditData[40].creditMaxOverdue|1740
# c|credit.creditBureau.creditData[40].creditOwner|0
# n|credit.creditBureau.creditData[40].creditProlong|0
# n|credit.creditBureau.creditData[40].creditSum|15010
# n|credit.creditBureau.creditData[40].creditSumDebt|0
# n|credit.creditBureau.creditData[40].creditSumLimit|0
# n|credit.creditBureau.creditData[40].creditSumOverdue|0
# n|credit.creditBureau.creditData[40].creditSumType|1
# n|credit.creditBureau.creditData[40].creditType|5
# c|credit.creditBureau.creditData[40].creditTypeUni|5
# d|credit.creditBureau.creditData[40].creditUpdate|22.08.2016 00:00:00
# n|credit.creditBureau.creditData[40].cuid|60268391
# n|credit.creditBureau.creditData[40].delay30|0
# n|credit.creditBureau.creditData[40].delay5|1
# n|credit.creditBureau.creditData[40].delay60|0
# n|credit.creditBureau.creditData[40].delay90|0
# n|credit.creditBureau.creditData[40].delayMore|0
# n|credit.creditBureau.creditData[41].cbAnnuity|0
# c|credit.creditBureau.creditData[41].cbOverdueLine|CCCCCCCCCCCC000000001000000000000000
# c|credit.creditBureau.creditData[41].contractSource|cb
# n|credit.creditBureau.creditData[41].cred_ratio|0
# n|credit.creditBureau.creditData[41].creditActive|0
# n|credit.creditBureau.creditData[41].creditCollateral|0
# n|credit.creditBureau.creditData[41].creditCostRate|18.94
# c|credit.creditBureau.creditData[41].creditCurrency|rur
# d|credit.creditBureau.creditData[41].creditDate|29.05.2017 00:00:00
# n|credit.creditBureau.creditData[41].creditDayOverdue|0
# d|credit.creditBureau.creditData[41].creditEndDate|29.05.2019 00:00:00
# d|credit.creditBureau.creditData[41].creditEndDateFact|30.05.2019 00:00:00
# n|credit.creditBureau.creditData[41].creditJoint|1
# n|credit.creditBureau.creditData[41].creditMaxOverdue|5389
# c|credit.creditBureau.creditData[41].creditOwner|0
# n|credit.creditBureau.creditData[41].creditProlong|0
# n|credit.creditBureau.creditData[41].creditSum|106600
# n|credit.creditBureau.creditData[41].creditSumDebt|0
# n|credit.creditBureau.creditData[41].creditSumLimit|0
# n|credit.creditBureau.creditData[41].creditSumOverdue|0
# n|credit.creditBureau.creditData[41].creditSumType|1
# n|credit.creditBureau.creditData[41].creditType|5
# c|credit.creditBureau.creditData[41].creditTypeUni|5
# d|credit.creditBureau.creditData[41].creditUpdate|02.06.2019 00:00:00
# n|credit.creditBureau.creditData[41].cuid|60268391
# n|credit.creditBureau.creditData[41].delay30|0
# n|credit.creditBureau.creditData[41].delay5|1
# n|credit.creditBureau.creditData[41].delay60|0
# n|credit.creditBureau.creditData[41].delay90|0
# n|credit.creditBureau.creditData[41].delayMore|0
# n|credit.creditBureau.creditData[42].cbAnnuity|3018
# c|credit.creditBureau.creditData[42].cbOverdueLine|-00000000000
# c|credit.creditBureau.creditData[42].contractSource|cb
# n|credit.creditBureau.creditData[42].cred_ratio|0
# n|credit.creditBureau.creditData[42].creditActive|1
# n|credit.creditBureau.creditData[42].creditCollateral|0
# n|credit.creditBureau.creditData[42].creditCostRate|19.94
# c|credit.creditBureau.creditData[42].creditCurrency|rur
# d|credit.creditBureau.creditData[42].creditDate|13.05.2019 00:00:00
# n|credit.creditBureau.creditData[42].creditDayOverdue|30
# d|credit.creditBureau.creditData[42].creditEndDate|13.03.2022 00:00:00
# n|credit.creditBureau.creditData[42].creditJoint|1
# n|credit.creditBureau.creditData[42].creditMaxOverdue|3025
# c|credit.creditBureau.creditData[42].creditOwner|0
# n|credit.creditBureau.creditData[42].creditProlong|0
# n|credit.creditBureau.creditData[42].creditSum|77951
# n|credit.creditBureau.creditData[42].creditSumDebt|60929
# n|credit.creditBureau.creditData[42].creditSumLimit|0
# n|credit.creditBureau.creditData[42].creditSumOverdue|3025
# n|credit.creditBureau.creditData[42].creditSumType|1
# n|credit.creditBureau.creditData[42].creditType|5
# c|credit.creditBureau.creditData[42].creditTypeUni|5
# d|credit.creditBureau.creditData[42].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[42].cuid|60268391
# n|credit.creditBureau.creditData[42].delay30|0
# n|credit.creditBureau.creditData[42].delay5|0
# n|credit.creditBureau.creditData[42].delay60|0
# n|credit.creditBureau.creditData[42].delay90|0
# n|credit.creditBureau.creditData[42].delayMore|0
# n|credit.creditBureau.creditData[43].cbAnnuity|0
# c|credit.creditBureau.creditData[43].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC000000
# c|credit.creditBureau.creditData[43].contractSource|cb
# n|credit.creditBureau.creditData[43].cred_ratio|0
# n|credit.creditBureau.creditData[43].creditActive|0
# n|credit.creditBureau.creditData[43].creditCollateral|0
# c|credit.creditBureau.creditData[43].creditCurrency|rur
# d|credit.creditBureau.creditData[43].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[43].creditDayOverdue|0
# d|credit.creditBureau.creditData[43].creditEndDate|03.04.2013 00:00:00
# d|credit.creditBureau.creditData[43].creditEndDateFact|03.04.2013 00:00:00
# n|credit.creditBureau.creditData[43].creditJoint|1
# n|credit.creditBureau.creditData[43].creditMaxOverdue|0
# c|credit.creditBureau.creditData[43].creditOwner|0
# n|credit.creditBureau.creditData[43].creditProlong|0
# n|credit.creditBureau.creditData[43].creditSum|11912
# n|credit.creditBureau.creditData[43].creditSumDebt|0
# n|credit.creditBureau.creditData[43].creditSumLimit|0
# n|credit.creditBureau.creditData[43].creditSumOverdue|0
# n|credit.creditBureau.creditData[43].creditSumType|1
# n|credit.creditBureau.creditData[43].creditType|5
# c|credit.creditBureau.creditData[43].creditTypeUni|5
# d|credit.creditBureau.creditData[43].creditUpdate|10.04.2013 00:00:00
# n|credit.creditBureau.creditData[43].cuid|60268391
# n|credit.creditBureau.creditData[43].delay30|0
# n|credit.creditBureau.creditData[43].delay5|0
# n|credit.creditBureau.creditData[43].delay60|0
# n|credit.creditBureau.creditData[43].delay90|0
# n|credit.creditBureau.creditData[43].delayMore|0
# n|credit.creditBureau.creditData[44].cbAnnuity|0
# c|credit.creditBureau.creditData[44].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCC--0------000000-0000-0000000000000000-0000000000---00000000000000
# c|credit.creditBureau.creditData[44].contractSource|cb
# n|credit.creditBureau.creditData[44].cred_ratio|0
# n|credit.creditBureau.creditData[44].creditActive|0
# n|credit.creditBureau.creditData[44].creditCollateral|0
# n|credit.creditBureau.creditData[44].creditCostRate|51.1
# c|credit.creditBureau.creditData[44].creditCurrency|rur
# d|credit.creditBureau.creditData[44].creditDate|03.10.2012 00:00:00
# n|credit.creditBureau.creditData[44].creditDayOverdue|0
# d|credit.creditBureau.creditData[44].creditEndDate|31.12.2099 00:00:00
# d|credit.creditBureau.creditData[44].creditEndDateFact|15.03.2018 00:00:00
# n|credit.creditBureau.creditData[44].creditJoint|1
# n|credit.creditBureau.creditData[44].creditMaxOverdue|0
# c|credit.creditBureau.creditData[44].creditOwner|0
# n|credit.creditBureau.creditData[44].creditProlong|0
# n|credit.creditBureau.creditData[44].creditSum|0
# n|credit.creditBureau.creditData[44].creditSumDebt|0
# n|credit.creditBureau.creditData[44].creditSumLimit|0
# n|credit.creditBureau.creditData[44].creditSumOverdue|0
# n|credit.creditBureau.creditData[44].creditSumType|1
# n|credit.creditBureau.creditData[44].creditType|4
# c|credit.creditBureau.creditData[44].creditTypeUni|4
# d|credit.creditBureau.creditData[44].creditUpdate|16.03.2018 00:00:00
# n|credit.creditBureau.creditData[44].cuid|60268391
# n|credit.creditBureau.creditData[44].delay30|0
# n|credit.creditBureau.creditData[44].delay5|0
# n|credit.creditBureau.creditData[44].delay60|0
# n|credit.creditBureau.creditData[44].delay90|0
# n|credit.creditBureau.creditData[44].delayMore|0
# n|credit.creditBureau.creditData[45].cbAnnuity|0
# c|credit.creditBureau.creditData[45].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC-0--
# c|credit.creditBureau.creditData[45].contractSource|cb
# n|credit.creditBureau.creditData[45].cred_ratio|0
# n|credit.creditBureau.creditData[45].creditActive|0
# n|credit.creditBureau.creditData[45].creditCollateral|0
# c|credit.creditBureau.creditData[45].creditCurrency|rur
# d|credit.creditBureau.creditData[45].creditDate|29.12.2011 00:00:00
# n|credit.creditBureau.creditData[45].creditDayOverdue|0
# d|credit.creditBureau.creditData[45].creditEndDate|02.04.2012 00:00:00
# d|credit.creditBureau.creditData[45].creditEndDateFact|02.04.2012 00:00:00
# n|credit.creditBureau.creditData[45].creditJoint|1
# n|credit.creditBureau.creditData[45].creditMaxOverdue|0
# c|credit.creditBureau.creditData[45].creditOwner|0
# n|credit.creditBureau.creditData[45].creditProlong|0
# n|credit.creditBureau.creditData[45].creditSum|3640
# n|credit.creditBureau.creditData[45].creditSumDebt|0
# n|credit.creditBureau.creditData[45].creditSumLimit|0
# n|credit.creditBureau.creditData[45].creditSumOverdue|0
# n|credit.creditBureau.creditData[45].creditSumType|1
# n|credit.creditBureau.creditData[45].creditType|5
# c|credit.creditBureau.creditData[45].creditTypeUni|5
# d|credit.creditBureau.creditData[45].creditUpdate|31.07.2012 00:00:00
# n|credit.creditBureau.creditData[45].cuid|60268391
# n|credit.creditBureau.creditData[45].delay30|0
# n|credit.creditBureau.creditData[45].delay5|0
# n|credit.creditBureau.creditData[45].delay60|0
# n|credit.creditBureau.creditData[45].delay90|0
# n|credit.creditBureau.creditData[45].delayMore|0
# n|credit.creditBureau.creditData[46].cbAnnuity|2168
# c|credit.creditBureau.creditData[46].cbOverdueLine|-000000000100000100
# c|credit.creditBureau.creditData[46].contractSource|cb
# n|credit.creditBureau.creditData[46].cred_ratio|0
# n|credit.creditBureau.creditData[46].creditActive|1
# n|credit.creditBureau.creditData[46].creditCollateral|0
# n|credit.creditBureau.creditData[46].creditCostRate|19.9
# c|credit.creditBureau.creditData[46].creditCurrency|rur
# d|credit.creditBureau.creditData[46].creditDate|17.10.2018 00:00:00
# n|credit.creditBureau.creditData[46].creditDayOverdue|30
# d|credit.creditBureau.creditData[46].creditEndDate|17.10.2020 00:00:00
# n|credit.creditBureau.creditData[46].creditJoint|1
# n|credit.creditBureau.creditData[46].creditMaxOverdue|2173
# c|credit.creditBureau.creditData[46].creditOwner|0
# n|credit.creditBureau.creditData[46].creditProlong|0
# n|credit.creditBureau.creditData[46].creditSum|42635
# n|credit.creditBureau.creditData[46].creditSumDebt|16498
# n|credit.creditBureau.creditData[46].creditSumLimit|0
# n|credit.creditBureau.creditData[46].creditSumOverdue|2173
# n|credit.creditBureau.creditData[46].creditSumType|1
# n|credit.creditBureau.creditData[46].creditType|5
# c|credit.creditBureau.creditData[46].creditTypeUni|5
# d|credit.creditBureau.creditData[46].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[46].cuid|60268391
# n|credit.creditBureau.creditData[46].delay30|0
# n|credit.creditBureau.creditData[46].delay5|2
# n|credit.creditBureau.creditData[46].delay60|0
# n|credit.creditBureau.creditData[46].delay90|0
# n|credit.creditBureau.creditData[46].delayMore|0
# n|credit.creditBureau.creditData[47].cbAnnuity|0
# c|credit.creditBureau.creditData[47].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC00000000000
# c|credit.creditBureau.creditData[47].contractSource|cb
# n|credit.creditBureau.creditData[47].cred_ratio|0
# n|credit.creditBureau.creditData[47].creditActive|0
# n|credit.creditBureau.creditData[47].creditCollateral|0
# n|credit.creditBureau.creditData[47].creditCostRate|36.49
# c|credit.creditBureau.creditData[47].creditCurrency|rur
# d|credit.creditBureau.creditData[47].creditDate|12.12.2016 00:00:00
# n|credit.creditBureau.creditData[47].creditDayOverdue|0
# d|credit.creditBureau.creditData[47].creditEndDate|12.02.2018 00:00:00
# d|credit.creditBureau.creditData[47].creditEndDateFact|13.11.2017 00:00:00
# n|credit.creditBureau.creditData[47].creditJoint|1
# n|credit.creditBureau.creditData[47].creditMaxOverdue|0
# c|credit.creditBureau.creditData[47].creditOwner|0
# n|credit.creditBureau.creditData[47].creditProlong|0
# n|credit.creditBureau.creditData[47].creditSum|18289
# n|credit.creditBureau.creditData[47].creditSumDebt|0
# n|credit.creditBureau.creditData[47].creditSumLimit|0
# n|credit.creditBureau.creditData[47].creditSumOverdue|0
# n|credit.creditBureau.creditData[47].creditSumType|1
# n|credit.creditBureau.creditData[47].creditType|5
# c|credit.creditBureau.creditData[47].creditTypeUni|5
# d|credit.creditBureau.creditData[47].creditUpdate|14.11.2017 00:00:00
# n|credit.creditBureau.creditData[47].cuid|60268391
# n|credit.creditBureau.creditData[47].delay30|0
# n|credit.creditBureau.creditData[47].delay5|0
# n|credit.creditBureau.creditData[47].delay60|0
# n|credit.creditBureau.creditData[47].delay90|0
# n|credit.creditBureau.creditData[47].delayMore|0
# n|credit.creditBureau.creditData[48].cbAnnuity|0
# c|credit.creditBureau.creditData[48].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC00000000000000000
# c|credit.creditBureau.creditData[48].contractSource|cb
# n|credit.creditBureau.creditData[48].cred_ratio|0
# n|credit.creditBureau.creditData[48].creditActive|0
# n|credit.creditBureau.creditData[48].creditCollateral|0
# n|credit.creditBureau.creditData[48].creditCostRate|22.02
# c|credit.creditBureau.creditData[48].creditCurrency|rur
# d|credit.creditBureau.creditData[48].creditDate|03.05.2016 00:00:00
# n|credit.creditBureau.creditData[48].creditDayOverdue|0
# d|credit.creditBureau.creditData[48].creditEndDate|03.05.2018 00:00:00
# d|credit.creditBureau.creditData[48].creditEndDateFact|24.10.2017 00:00:00
# n|credit.creditBureau.creditData[48].creditJoint|1
# n|credit.creditBureau.creditData[48].creditMaxOverdue|0
# c|credit.creditBureau.creditData[48].creditOwner|0
# n|credit.creditBureau.creditData[48].creditProlong|0
# n|credit.creditBureau.creditData[48].creditSum|37717
# n|credit.creditBureau.creditData[48].creditSumDebt|0
# n|credit.creditBureau.creditData[48].creditSumLimit|0
# n|credit.creditBureau.creditData[48].creditSumOverdue|0
# n|credit.creditBureau.creditData[48].creditSumType|1
# n|credit.creditBureau.creditData[48].creditType|5
# c|credit.creditBureau.creditData[48].creditTypeUni|5
# d|credit.creditBureau.creditData[48].creditUpdate|15.05.2019 00:00:00
# n|credit.creditBureau.creditData[48].cuid|60268391
# n|credit.creditBureau.creditData[48].delay30|0
# n|credit.creditBureau.creditData[48].delay5|0
# n|credit.creditBureau.creditData[48].delay60|0
# n|credit.creditBureau.creditData[48].delay90|0
# n|credit.creditBureau.creditData[48].delayMore|0
# n|credit.creditBureau.creditData[49].cbAnnuity|0
# c|credit.creditBureau.creditData[49].cbOverdueLine|CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC111111111110101011101000
# c|credit.creditBureau.creditData[49].contractSource|cb
# n|credit.creditBureau.creditData[49].cred_ratio|0
# n|credit.creditBureau.creditData[49].creditActive|0
# n|credit.creditBureau.creditData[49].creditCollateral|0
# n|credit.creditBureau.creditData[49].creditCostRate|24.57
# c|credit.creditBureau.creditData[49].creditCurrency|rur
# d|credit.creditBureau.creditData[49].creditDate|07.05.2015 00:00:00
# n|credit.creditBureau.creditData[49].creditDayOverdue|0
# d|credit.creditBureau.creditData[49].creditEndDate|07.05.2017 00:00:00
# d|credit.creditBureau.creditData[49].creditEndDateFact|13.05.2017 00:00:00
# n|credit.creditBureau.creditData[49].creditJoint|1
# n|credit.creditBureau.creditData[49].creditMaxOverdue|5651
# c|credit.creditBureau.creditData[49].creditOwner|0
# n|credit.creditBureau.creditData[49].creditProlong|0
# n|credit.creditBureau.creditData[49].creditSum|106400
# n|credit.creditBureau.creditData[49].creditSumDebt|0
# n|credit.creditBureau.creditData[49].creditSumLimit|0
# n|credit.creditBureau.creditData[49].creditSumOverdue|0
# n|credit.creditBureau.creditData[49].creditSumType|1
# n|credit.creditBureau.creditData[49].creditType|5
# c|credit.creditBureau.creditData[49].creditTypeUni|5
# d|credit.creditBureau.creditData[49].creditUpdate|15.05.2019 00:00:00
# n|credit.creditBureau.creditData[49].cuid|60268391
# n|credit.creditBureau.creditData[49].delay30|0
# n|credit.creditBureau.creditData[49].delay5|17
# n|credit.creditBureau.creditData[49].delay60|0
# n|credit.creditBureau.creditData[49].delay90|0
# n|credit.creditBureau.creditData[49].delayMore|0
# n|credit.creditBureau.creditData[50].cbAnnuity|1128
# c|credit.creditBureau.creditData[50].cbOverdueLine|-001100000000000100010000
# c|credit.creditBureau.creditData[50].contractSource|cb
# n|credit.creditBureau.creditData[50].cred_ratio|0
# n|credit.creditBureau.creditData[50].creditActive|1
# n|credit.creditBureau.creditData[50].creditCollateral|0
# n|credit.creditBureau.creditData[50].creditCostRate|17.36
# c|credit.creditBureau.creditData[50].creditCurrency|rur
# d|credit.creditBureau.creditData[50].creditDate|05.04.2018 00:00:00
# n|credit.creditBureau.creditData[50].creditDayOverdue|30
# d|credit.creditBureau.creditData[50].creditEndDate|05.04.2021 00:00:00
# n|credit.creditBureau.creditData[50].creditJoint|1
# n|credit.creditBureau.creditData[50].creditMaxOverdue|1131
# c|credit.creditBureau.creditData[50].creditOwner|0
# n|credit.creditBureau.creditData[50].creditProlong|0
# n|credit.creditBureau.creditData[50].creditSum|31490
# n|credit.creditBureau.creditData[50].creditSumDebt|13577
# n|credit.creditBureau.creditData[50].creditSumLimit|0
# n|credit.creditBureau.creditData[50].creditSumOverdue|1131
# n|credit.creditBureau.creditData[50].creditSumType|1
# n|credit.creditBureau.creditData[50].creditType|5
# c|credit.creditBureau.creditData[50].creditTypeUni|5
# d|credit.creditBureau.creditData[50].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[50].cuid|60268391
# n|credit.creditBureau.creditData[50].delay30|0
# n|credit.creditBureau.creditData[50].delay5|4
# n|credit.creditBureau.creditData[50].delay60|0
# n|credit.creditBureau.creditData[50].delay90|0
# n|credit.creditBureau.creditData[50].delayMore|0
# c|credit.creditBureau.creditData[51].contractSource|cb
# n|credit.creditBureau.creditData[51].cred_ratio|0
# n|credit.creditBureau.creditData[51].creditActive|0
# n|credit.creditBureau.creditData[51].creditCollateral|0
# c|credit.creditBureau.creditData[51].creditCurrency|rur
# d|credit.creditBureau.creditData[51].creditDate|15.05.2009 00:00:00
# n|credit.creditBureau.creditData[51].creditDayOverdue|0
# d|credit.creditBureau.creditData[51].creditEndDate|16.11.2009 00:00:00
# d|credit.creditBureau.creditData[51].creditEndDateFact|17.08.2009 00:00:00
# n|credit.creditBureau.creditData[51].creditJoint|1
# n|credit.creditBureau.creditData[51].creditMaxOverdue|0
# c|credit.creditBureau.creditData[51].creditOwner|0
# n|credit.creditBureau.creditData[51].creditProlong|0
# n|credit.creditBureau.creditData[51].creditSum|12990
# n|credit.creditBureau.creditData[51].creditSumDebt|0
# n|credit.creditBureau.creditData[51].creditSumLimit|0
# n|credit.creditBureau.creditData[51].creditSumOverdue|0
# n|credit.creditBureau.creditData[51].creditSumType|1
# n|credit.creditBureau.creditData[51].creditType|5
# c|credit.creditBureau.creditData[51].creditTypeUni|5
# d|credit.creditBureau.creditData[51].creditUpdate|17.08.2009 00:00:00
# n|credit.creditBureau.creditData[51].cuid|60268391
# n|credit.creditBureau.creditData[51].delay30|0
# n|credit.creditBureau.creditData[51].delay5|0
# n|credit.creditBureau.creditData[51].delay60|0
# n|credit.creditBureau.creditData[51].delay90|0
# n|credit.creditBureau.creditData[51].delayMore|0
# n|credit.creditBureau.creditData[52].cbAnnuity|0
# c|credit.creditBureau.creditData[52].cbOverdueLine|0
# c|credit.creditBureau.creditData[52].contractSource|cb
# n|credit.creditBureau.creditData[52].cred_ratio|0
# n|credit.creditBureau.creditData[52].creditActive|1
# n|credit.creditBureau.creditData[52].creditCollateral|0
# n|credit.creditBureau.creditData[52].creditCostRate|28.75
# c|credit.creditBureau.creditData[52].creditCurrency|rur
# d|credit.creditBureau.creditData[52].creditDate|20.04.2020 00:00:00
# n|credit.creditBureau.creditData[52].creditDayOverdue|0
# d|credit.creditBureau.creditData[52].creditEndDate|28.02.2025 00:00:00
# n|credit.creditBureau.creditData[52].creditJoint|1
# n|credit.creditBureau.creditData[52].creditMaxOverdue|0
# c|credit.creditBureau.creditData[52].creditOwner|0
# n|credit.creditBureau.creditData[52].creditProlong|0
# n|credit.creditBureau.creditData[52].creditSum|5000
# n|credit.creditBureau.creditData[52].creditSumDebt|4953
# n|credit.creditBureau.creditData[52].creditSumLimit|47
# n|credit.creditBureau.creditData[52].creditSumOverdue|0
# n|credit.creditBureau.creditData[52].creditSumType|1
# n|credit.creditBureau.creditData[52].creditType|4
# c|credit.creditBureau.creditData[52].creditTypeUni|4
# d|credit.creditBureau.creditData[52].creditUpdate|05.05.2020 00:00:00
# n|credit.creditBureau.creditData[52].cuid|60268391
# n|credit.creditBureau.creditData[52].delay30|0
# n|credit.creditBureau.creditData[52].delay5|0
# n|credit.creditBureau.creditData[52].delay60|0
# n|credit.creditBureau.creditData[52].delay90|0
# n|credit.creditBureau.creditData[52].delayMore|0
# n|credit.creditBureau.creditData[53].cbAnnuity|1137
# c|credit.creditBureau.creditData[53].cbOverdueLine|-000000000000000000010000000000
# c|credit.creditBureau.creditData[53].contractSource|cb
# n|credit.creditBureau.creditData[53].cred_ratio|0
# n|credit.creditBureau.creditData[53].creditActive|1
# n|credit.creditBureau.creditData[53].creditCollateral|0
# n|credit.creditBureau.creditData[53].creditCostRate|19.9
# c|credit.creditBureau.creditData[53].creditCurrency|rur
# d|credit.creditBureau.creditData[53].creditDate|24.10.2017 00:00:00
# n|credit.creditBureau.creditData[53].creditDayOverdue|30
# d|credit.creditBureau.creditData[53].creditEndDate|24.10.2022 00:00:00
# n|credit.creditBureau.creditData[53].creditJoint|1
# n|credit.creditBureau.creditData[53].creditMaxOverdue|1141
# c|credit.creditBureau.creditData[53].creditOwner|0
# n|credit.creditBureau.creditData[53].creditProlong|0
# n|credit.creditBureau.creditData[53].creditSum|43000
# n|credit.creditBureau.creditData[53].creditSumDebt|28756
# n|credit.creditBureau.creditData[53].creditSumLimit|0
# n|credit.creditBureau.creditData[53].creditSumOverdue|1139
# n|credit.creditBureau.creditData[53].creditSumType|1
# n|credit.creditBureau.creditData[53].creditType|5
# c|credit.creditBureau.creditData[53].creditTypeUni|5
# d|credit.creditBureau.creditData[53].creditUpdate|11.05.2020 00:00:00
# n|credit.creditBureau.creditData[53].cuid|60268391
# n|credit.creditBureau.creditData[53].delay30|0
# n|credit.creditBureau.creditData[53].delay5|1
# n|credit.creditBureau.creditData[53].delay60|0
# n|credit.creditBureau.creditData[53].delay90|0
# n|credit.creditBureau.creditData[53].delayMore|0
# n|credit.creditBureau.creditData[54].cbAnnuity|4488
# c|credit.creditBureau.creditData[54].contractSource|cb
# n|credit.creditBureau.creditData[54].cred_ratio|0
# n|credit.creditBureau.creditData[54].creditActive|1
# n|credit.creditBureau.creditData[54].creditCollateral|0
# n|credit.creditBureau.creditData[54].creditCostRate|22.9
# c|credit.creditBureau.creditData[54].creditCurrency|rur
# d|credit.creditBureau.creditData[54].creditDate|14.09.2018 00:00:00
# n|credit.creditBureau.creditData[54].creditDayOverdue|0
# d|credit.creditBureau.creditData[54].creditEndDate|16.12.2021 00:00:00
# n|credit.creditBureau.creditData[54].creditJoint|1
# n|credit.creditBureau.creditData[54].creditMaxOverdue|1541.24
# c|credit.creditBureau.creditData[54].creditOwner|0
# n|credit.creditBureau.creditData[54].creditProlong|3
# n|credit.creditBureau.creditData[54].creditSum|58224
# n|credit.creditBureau.creditData[54].creditSumDebt|37685.46
# n|credit.creditBureau.creditData[54].creditSumLimit|0
# n|credit.creditBureau.creditData[54].creditSumOverdue|0
# n|credit.creditBureau.creditData[54].creditSumType|1
# n|credit.creditBureau.creditData[54].creditType|5
# c|credit.creditBureau.creditData[54].creditTypeUni|5
# d|credit.creditBureau.creditData[54].creditUpdate|09.05.2020 00:00:00
# n|credit.creditBureau.creditData[54].cuid|60268391
# n|credit.creditBureau.creditData[54].delay30|0
# n|credit.creditBureau.creditData[54].delay5|7
# n|credit.creditBureau.creditData[54].delay60|0
# n|credit.creditBureau.creditData[54].delay90|0
# n|credit.creditBureau.creditData[54].delayMore|0