from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory
from incf.countryutils import data as countrydata
from dexterity.membrane import _


province_type=[
                  ('Hunan','Hunan',_(u'Hunan')),
                  ('hubei','hubei',_(u'Hubei')),
                  ('beijing','beijing',_(u'Beijing')),
                  ('heilongjiang','heilongjiang',_(u'heilongjiang')),
                  ('jilin','jilin',_(u'Jilin')),  
                  ('liaolin','liaolin',_(u'liaolin')),
                  ('shandong','shandong',_(u'Shandong')),
                  ('shanxi','shanxi',_(u'Shanxi')),
                  ('hebei','hebei',_(u'Heber')),
                  ('henan','henan',_(u'Henan')),
                  ('neimenggu','neimenggu',_(u'Neimenggu')),  
                  ('xinqiang','xinqiang',_(u'Xinqiang')),
                  ('Qinghai','Qinghai',_(u'Qinghai')),
                  ('Xizang','Xizang',_(u'Xizang')),
                  ('Shanxi','Shanxi',_(u'Shanxi')),
                  ('Tianjin','Tianjin',_(u'Tianjin')),
                  ('Shanghai','Shanghai',_(u'Shanghai')),  
                  ('Anhui','Anhui',_(u'Anhui')),
                  ('Jiangsu','Jiangsu',_(u'Jiangsu')),
                  ('Zhejiang','Zhejiang',_(u'Zhejiang')),
                  ('Sichuan','Sichuan',_(u'Sichuan')),
                  ('Fujian','Fujian',_(u'Fujian')),
                  ('Guangdong','Guangdong',_(u'Guangdong')),  
                  ('Guangxi','Guangxi',_(u'Guangxi')),
                  ('Yunnan','Yunnan',_(u'yunnan')),
                  ('Guizhou','Guizhou',_(u'Guizhou')),
                  ('Shenzhen','Shenzhen',_(u'Shenzhen')),
                  ('Xianggang','Xianggang',_(u'Xianggang')),
                  ('Aomen','Aomen',_(u'Aomen')),  
                  ('Taiwan','Taiwan',_(u'Taiwan')),
                  ('Chongqing','Chongqing',_(u'Chongqing')),
                  ('Jiangxi','Jiangxi',_(u'Jiangxi')),
                  ('Ningxia','Ningxia',_(u'Ningxia')),
                  ('Gansu','Gansu',_(u'Gansu')),
                  ('Hainan','Hainan',_(u'Hainan')),                                                                                                            
                        ]
province_type_terms = [SimpleTerm(value, token, title) for value, token, title in province_type ]

class ProvinceTypes(object):

    def __call__(self, context):
        return SimpleVocabulary(province_type_terms)

grok.global_utility(ProvinceTypes, IVocabularyFactory,
        name="dexterity.membrane.vocabulary.province")

sector_type=[('education','education',_(u'Education')),
               ('government','government',_(u'Government')),
               ('finance','finance',_(u'Finance')),
               ('energy','energy',_(u'energy')),
               ('consult','consult',_(u'consult')),
               ('manufacture','manufacture',_(u'manufacture')),
               ('telecommunication','telecommunication',_(u'telecommunication')),
               ('enterprise','enterprise',_(u'enterprise')),
               ]
               
sector_type_terms = [SimpleTerm(value, token, title) for value, token, title in sector_type ]

class SectorTypes(object):

    def __call__(self, context):
        return SimpleVocabulary(sector_type_terms)

grok.global_utility(SectorTypes, IVocabularyFactory,
        name="dexterity.membrane.vocabulary.sector")





