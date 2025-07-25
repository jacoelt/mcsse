export type Country = {
  name: string;
  code: string;
  flag: string;
};


function countryCodeToFlag(countryCode: string): string {
  const offset = 127397;
  const flag = Array.from(countryCode).map((letter:string) => String.fromCodePoint(letter.charCodeAt(0) + offset)).join('');

  return flag;
}


const COUNTRY_MAPPING: Record<string, Country> = {
  'AF': {name : 'Afghanistan', code: 'AF', flag: countryCodeToFlag('AF')},
  'AL': {name : 'Albania', code: 'AL', flag: countryCodeToFlag('AL')},
  'DZ': {name : 'Algeria', code: 'DZ', flag: countryCodeToFlag('DZ')},
  'AS': {name : 'American Samoa', code: 'AS', flag: countryCodeToFlag('AS')},
  'AD': {name : 'Andorra', code: 'AD', flag: countryCodeToFlag('AD')},
  'AO': {name : 'Angola', code: 'AO', flag: countryCodeToFlag('AO')},
  'AI': {name : 'Anguilla', code: 'AI', flag: countryCodeToFlag('AI')},
  'AQ': {name : 'Antarctica', code: 'AQ', flag: countryCodeToFlag('AQ')},
  'AG': {name : 'Antigua and Barbuda', code: 'AG', flag: countryCodeToFlag('AG')},
  'AR': {name : 'Argentina', code: 'AR', flag: countryCodeToFlag('AR')},
  'AM': {name : 'Armenia', code: 'AM', flag: countryCodeToFlag('AM')},
  'AW': {name : 'Aruba', code: 'AW', flag: countryCodeToFlag('AW')},
  'AU': {name : 'Australia', code: 'AU', flag: countryCodeToFlag('AU')},
  'AT': {name : 'Austria', code: 'AT', flag: countryCodeToFlag('AT')},
  'AZ': {name : 'Azerbaijan', code: 'AZ', flag: countryCodeToFlag('AZ')},
  'BS': {name : 'Bahamas (the)', code: 'BS', flag: countryCodeToFlag('BS')},
  'BH': {name : 'Bahrain', code: 'BH', flag: countryCodeToFlag('BH')},
  'BD': {name : 'Bangladesh', code: 'BD', flag: countryCodeToFlag('BD')},
  'BB': {name : 'Barbados', code: 'BB', flag: countryCodeToFlag('BB')},
  'BY': {name : 'Belarus', code: 'BY', flag: countryCodeToFlag('BY')},
  'BE': {name : 'Belgium', code: 'BE', flag: countryCodeToFlag('BE')},
  'BZ': {name : 'Belize', code: 'BZ', flag: countryCodeToFlag('BZ')},
  'BJ': {name : 'Benin', code: 'BJ', flag: countryCodeToFlag('BJ')},
  'BM': {name : 'Bermuda', code: 'BM', flag: countryCodeToFlag('BM')},
  'BT': {name : 'Bhutan', code: 'BT', flag: countryCodeToFlag('BT')},
  'BO': {name : 'Bolivia (Plurinational State of)', code: 'BO', flag: countryCodeToFlag('BO')},
  'BQ': {name : 'Bonaire, Sint Eustatius and Saba', code: 'BQ', flag: countryCodeToFlag('BQ')},
  'BA': {name : 'Bosnia and Herzegovina', code: 'BA', flag: countryCodeToFlag('BA')},
  'BW': {name : 'Botswana', code: 'BW', flag: countryCodeToFlag('BW')},
  'BV': {name : 'Bouvet Island', code: 'BV', flag: countryCodeToFlag('BV')},
  'BR': {name : 'Brazil', code: 'BR', flag: countryCodeToFlag('BR')},
  'IO': {name : 'British Indian Ocean Territory (the)', code: 'IO', flag: countryCodeToFlag('IO')},
  'BN': {name : 'Brunei Darussalam', code: 'BN', flag: countryCodeToFlag('BN')},
  'BG': {name : 'Bulgaria', code: 'BG', flag: countryCodeToFlag('BG')},
  'BF': {name : 'Burkina Faso', code: 'BF', flag: countryCodeToFlag('BF')},
  'BI': {name : 'Burundi', code: 'BI', flag: countryCodeToFlag('BI')},
  'CV': {name : 'Cabo Verde', code: 'CV', flag: countryCodeToFlag('CV')},
  'KH': {name : 'Cambodia', code: 'KH', flag: countryCodeToFlag('KH')},
  'CM': {name : 'Cameroon', code: 'CM', flag: countryCodeToFlag('CM')},
  'CA': {name : 'Canada', code: 'CA', flag: countryCodeToFlag('CA')},
  'KY': {name : 'Cayman Islands (the)', code: 'KY', flag: countryCodeToFlag('KY')},
  'CF': {name : 'Central African Republic (the)', code: 'CF', flag: countryCodeToFlag('CF')},
  'TD': {name : 'Chad', code: 'TD', flag: countryCodeToFlag('TD')},
  'CL': {name : 'Chile', code: 'CL', flag: countryCodeToFlag('CL')},
  'CN': {name : 'China', code: 'CN', flag: countryCodeToFlag('CN')},
  'CX': {name : 'Christmas Island', code: 'CX', flag: countryCodeToFlag('CX')},
  'CC': {name : 'Cocos (Keeling) Islands (the)', code: 'CC', flag: countryCodeToFlag('CC')},
  'CO': {name : 'Colombia', code: 'CO', flag: countryCodeToFlag('CO')},
  'KM': {name : 'Comoros (the)', code: 'KM', flag: countryCodeToFlag('KM')},
  'CD': {name : 'Congo (the Democratic Republic of the)', code: 'CD', flag: countryCodeToFlag('CD')},
  'CG': {name : 'Congo (the)', code: 'CG', flag: countryCodeToFlag('CG')},
  'CK': {name : 'Cook Islands (the)', code: 'CK', flag: countryCodeToFlag('CK')},
  'CR': {name : 'Costa Rica', code: 'CR', flag: countryCodeToFlag('CR')},
  'HR': {name : 'Croatia', code: 'HR', flag: countryCodeToFlag('HR')},
  'CU': {name : 'Cuba', code: 'CU', flag: countryCodeToFlag('CU')},
  'CW': {name : 'Curaçao', code: 'CW', flag: countryCodeToFlag('CW')},
  'CY': {name : 'Cyprus', code: 'CY', flag: countryCodeToFlag('CY')},
  'CZ': {name : 'Czechia', code: 'CZ', flag: countryCodeToFlag('CZ')},
  'CI': {name : 'Côte d\'Ivoire', code: 'CI', flag: countryCodeToFlag('CI')},
  'DK': {name : 'Denmark', code: 'DK', flag: countryCodeToFlag('DK')},
  'DJ': {name : 'Djibouti', code: 'DJ', flag: countryCodeToFlag('DJ')},
  'DM': {name : 'Dominica', code: 'DM', flag: countryCodeToFlag('DM')},
  'DO': {name : 'Dominican Republic (the)', code: 'DO', flag: countryCodeToFlag('DO')},
  'EC': {name : 'Ecuador', code: 'EC', flag: countryCodeToFlag('EC')},
  'EG': {name : 'Egypt', code: 'EG', flag: countryCodeToFlag('EG')},
  'SV': {name : 'El Salvador', code: 'SV', flag: countryCodeToFlag('SV')},
  'GQ': {name : 'Equatorial Guinea', code: 'GQ', flag: countryCodeToFlag('GQ')},
  'ER': {name : 'Eritrea', code: 'ER', flag: countryCodeToFlag('ER')},
  'EE': {name : 'Estonia', code: 'EE', flag: countryCodeToFlag('EE')},
  'SZ': {name : 'Eswatini', code: 'SZ', flag: countryCodeToFlag('SZ')},
  'ET': {name : 'Ethiopia', code: 'ET', flag: countryCodeToFlag('ET')},
  'FK': {name : 'Falkland Islands (the) [Malvinas]', code: 'FK', flag: countryCodeToFlag('FK')},
  'FO': {name : 'Faroe Islands (the)', code: 'FO', flag: countryCodeToFlag('FO')},
  'FJ': {name : 'Fiji', code: 'FJ', flag: countryCodeToFlag('FJ')},
  'FI': {name : 'Finland', code: 'FI', flag: countryCodeToFlag('FI')},
  'FR': {name : 'France', code: 'FR', flag: countryCodeToFlag('FR')},
  'GF': {name : 'French Guiana', code: 'GF', flag: countryCodeToFlag('GF')},
  'PF': {name : 'French Polynesia', code: 'PF', flag: countryCodeToFlag('PF')},
  'TF': {name : 'French Southern Territories (the)', code: 'TF', flag: countryCodeToFlag('TF')},
  'GA': {name : 'Gabon', code: 'GA', flag: countryCodeToFlag('GA')},
  'GM': {name : 'Gambia (the)', code: 'GM', flag: countryCodeToFlag('GM')},
  'GE': {name : 'Georgia', code: 'GE', flag: countryCodeToFlag('GE')},
  'DE': {name : 'Germany', code: 'DE', flag: countryCodeToFlag('DE')},
  'GH': {name : 'Ghana', code: 'GH', flag: countryCodeToFlag('GH')},
  'GI': {name : 'Gibraltar', code: 'GI', flag: countryCodeToFlag('GI')},
  'GR': {name : 'Greece', code: 'GR', flag: countryCodeToFlag('GR')},
  'GL': {name : 'Greenland', code: 'GL', flag: countryCodeToFlag('GL')},
  'GD': {name : 'Grenada', code: 'GD', flag: countryCodeToFlag('GD')},
  'GP': {name : 'Guadeloupe', code: 'GP', flag: countryCodeToFlag('GP')},
  'GU': {name : 'Guam', code: 'GU', flag: countryCodeToFlag('GU')},
  'GT': {name : 'Guatemala', code: 'GT', flag: countryCodeToFlag('GT')},
  'GG': {name : 'Guernsey', code: 'GG', flag: countryCodeToFlag('GG')},
  'GN': {name : 'Guinea', code: 'GN', flag: countryCodeToFlag('GN')},
  'GW': {name : 'Guinea-Bissau', code: 'GW', flag: countryCodeToFlag('GW')},
  'GY': {name : 'Guyana', code: 'GY', flag: countryCodeToFlag('GY')},
  'HT': {name : 'Haiti', code: 'HT', flag: countryCodeToFlag('HT')},
  'HM': {name : 'Heard Island and McDonald Islands', code: 'HM', flag: countryCodeToFlag('HM')},
  'VA': {name : 'Holy See (the)', code: 'VA', flag: countryCodeToFlag('VA')},
  'HN': {name : 'Honduras', code: 'HN', flag: countryCodeToFlag('HN')},
  'HK': {name : 'Hong Kong', code: 'HK', flag: countryCodeToFlag('HK')},
  'HU': {name : 'Hungary', code: 'HU', flag: countryCodeToFlag('HU')},
  'IS': {name : 'Iceland', code: 'IS', flag: countryCodeToFlag('IS')},
  'IN': {name : 'India', code: 'IN', flag: countryCodeToFlag('IN')},
  'ID': {name : 'Indonesia', code: 'ID', flag: countryCodeToFlag('ID')},
  'IR': {name : 'Iran (Islamic Republic of)', code: 'IR', flag: countryCodeToFlag('IR')},
  'IQ': {name : 'Iraq', code: 'IQ', flag: countryCodeToFlag('IQ')},
  'IE': {name : 'Ireland', code: 'IE', flag: countryCodeToFlag('IE')},
  'IM': {name : 'Isle of Man', code: 'IM', flag: countryCodeToFlag('IM')},
  'IL': {name : 'Israel', code: 'IL', flag: countryCodeToFlag('IL')},
  'IT': {name : 'Italy', code: 'IT', flag: countryCodeToFlag('IT')},
  'JM': {name : 'Jamaica', code: 'JM', flag: countryCodeToFlag('JM')},
  'JP': {name : 'Japan', code: 'JP', flag: countryCodeToFlag('JP')},
  'JE': {name : 'Jersey', code: 'JE', flag: countryCodeToFlag('JE')},
  'JO': {name : 'Jordan', code: 'JO', flag: countryCodeToFlag('JO')},
  'KZ': {name : 'Kazakhstan', code: 'KZ', flag: countryCodeToFlag('KZ')},
  'KE': {name : 'Kenya', code: 'KE', flag: countryCodeToFlag('KE')},
  'KI': {name : 'Kiribati', code: 'KI', flag: countryCodeToFlag('KI')},
  'KP': {name : 'Korea (the Democratic People\'s Republic of)', code: 'KP', flag: countryCodeToFlag('KP')},
  'KR': {name : 'Korea (the Republic of)', code: 'KR', flag: countryCodeToFlag('KR')},
  'KW': {name : 'Kuwait', code: 'KW', flag: countryCodeToFlag('KW')},
  'KG': {name : 'Kyrgyzstan', code: 'KG', flag: countryCodeToFlag('KG')},
  'LA': {name : 'Lao People\'s Democratic Republic (the)', code: 'LA', flag: countryCodeToFlag('LA')},
  'LV': {name : 'Latvia', code: 'LV', flag: countryCodeToFlag('LV')},
  'LB': {name : 'Lebanon', code: 'LB', flag: countryCodeToFlag('LB')},
  'LS': {name : 'Lesotho', code: 'LS', flag: countryCodeToFlag('LS')},
  'LR': {name : 'Liberia', code: 'LR', flag: countryCodeToFlag('LR')},
  'LY': {name : 'Libya', code: 'LY', flag: countryCodeToFlag('LY')},
  'LI': {name : 'Liechtenstein', code: 'LI', flag: countryCodeToFlag('LI')},
  'LT': {name : 'Lithuania', code: 'LT', flag: countryCodeToFlag('LT')},
  'LU': {name : 'Luxembourg', code: 'LU', flag: countryCodeToFlag('LU')},
  'MO': {name : 'Macao', code: 'MO', flag: countryCodeToFlag('MO')},
  'MG': {name : 'Madagascar', code: 'MG', flag: countryCodeToFlag('MG')},
  'MW': {name : 'Malawi', code: 'MW', flag: countryCodeToFlag('MW')},
  'MY': {name : 'Malaysia', code: 'MY', flag: countryCodeToFlag('MY')},
  'MV': {name : 'Maldives', code: 'MV', flag: countryCodeToFlag('MV')},
  'ML': {name : 'Mali', code: 'ML', flag: countryCodeToFlag('ML')},
  'MT': {name : 'Malta', code: 'MT', flag: countryCodeToFlag('MT')},
  'MH': {name : 'Marshall Islands (the)', code: 'MH', flag: countryCodeToFlag('MH')},
  'MQ': {name : 'Martinique', code: 'MQ', flag: countryCodeToFlag('MQ')},
  'MR': {name : 'Mauritania', code: 'MR', flag: countryCodeToFlag('MR')},
  'MU': {name : 'Mauritius', code: 'MU', flag: countryCodeToFlag('MU')},
  'YT': {name : 'Mayotte', code: 'YT', flag: countryCodeToFlag('YT')},
  'MX': {name : 'Mexico', code: 'MX', flag: countryCodeToFlag('MX')},
  'FM': {name : 'Micronesia (Federated States of)', code: 'FM', flag: countryCodeToFlag('FM')},
  'MD': {name : 'Moldova (the Republic of)', code: 'MD', flag: countryCodeToFlag('MD')},
  'MC': {name : 'Monaco', code: 'MC', flag: countryCodeToFlag('MC')},
  'MN': {name : 'Mongolia', code: 'MN', flag: countryCodeToFlag('MN')},
  'ME': {name : 'Montenegro', code: 'ME', flag: countryCodeToFlag('ME')},
  'MS': {name : 'Montserrat', code: 'MS', flag: countryCodeToFlag('MS')},
  'MA': {name : 'Morocco', code: 'MA', flag: countryCodeToFlag('MA')},
  'MZ': {name : 'Mozambique', code: 'MZ', flag: countryCodeToFlag('MZ')},
  'MM': {name : 'Myanmar', code: 'MM', flag: countryCodeToFlag('MM')},
  'NA': {name : 'Namibia', code: 'NA', flag: countryCodeToFlag('NA')},
  'NR': {name : 'Nauru', code: 'NR', flag: countryCodeToFlag('NR')},
  'NP': {name : 'Nepal', code: 'NP', flag: countryCodeToFlag('NP')},
  'NL': {name : 'Netherlands (the)', code: 'NL', flag: countryCodeToFlag('NL')},
  'NC': {name : 'New Caledonia', code: 'NC', flag: countryCodeToFlag('NC')},
  'NZ': {name : 'New Zealand', code: 'NZ', flag: countryCodeToFlag('NZ')},
  'NI': {name : 'Nicaragua', code: 'NI', flag: countryCodeToFlag('NI')},
  'NE': {name : 'Niger (the)', code: 'NE', flag: countryCodeToFlag('NE')},
  'NG': {name : 'Nigeria', code: 'NG', flag: countryCodeToFlag('NG')},
  'NU': {name : 'Niue', code: 'NU', flag: countryCodeToFlag('NU')},
  'NF': {name : 'Norfolk Island', code: 'NF', flag: countryCodeToFlag('NF')},
  'MP': {name : 'Northern Mariana Islands (the)', code: 'MP', flag: countryCodeToFlag('MP')},
  'NO': {name : 'Norway', code: 'NO', flag: countryCodeToFlag('NO')},
  'OM': {name : 'Oman', code: 'OM', flag: countryCodeToFlag('OM')},
  'PK': {name : 'Pakistan', code: 'PK', flag: countryCodeToFlag('PK')},
  'PW': {name : 'Palau', code: 'PW', flag: countryCodeToFlag('PW')},
  'PS': {name : 'Palestine, State of', code: 'PS', flag: countryCodeToFlag('PS')},
  'PA': {name : 'Panama', code: 'PA', flag: countryCodeToFlag('PA')},
  'PG': {name : 'Papua New Guinea', code: 'PG', flag: countryCodeToFlag('PG')},
  'PY': {name : 'Paraguay', code: 'PY', flag: countryCodeToFlag('PY')},
  'PE': {name : 'Peru', code: 'PE', flag: countryCodeToFlag('PE')},
  'PH': {name : 'Philippines (the)', code: 'PH', flag: countryCodeToFlag('PH')},
  'PN': {name : 'Pitcairn', code: 'PN', flag: countryCodeToFlag('PN')},
  'PL': {name : 'Poland', code: 'PL', flag: countryCodeToFlag('PL')},
  'PT': {name : 'Portugal', code: 'PT', flag: countryCodeToFlag('PT')},
  'PR': {name : 'Puerto Rico', code: 'PR', flag: countryCodeToFlag('PR')},
  'QA': {name : 'Qatar', code: 'QA', flag: countryCodeToFlag('QA')},
  'MK': {name : 'Republic of North Macedonia', code: 'MK', flag: countryCodeToFlag('MK')},
  'RO': {name : 'Romania', code: 'RO', flag: countryCodeToFlag('RO')},
  'RU': {name : 'Russian Federation (the)', code: 'RU', flag: countryCodeToFlag('RU')},
  'RW': {name : 'Rwanda', code: 'RW', flag: countryCodeToFlag('RW')},
  'RE': {name : 'Réunion', code: 'RE', flag: countryCodeToFlag('RE')},
  'BL': {name : 'Saint Barthélemy', code: 'BL', flag: countryCodeToFlag('BL')},
  'SH': {name : 'Saint Helena, Ascension and Tristan da Cunha', code: 'SH', flag: countryCodeToFlag('SH')},
  'KN': {name : 'Saint Kitts and Nevis', code: 'KN', flag: countryCodeToFlag('KN')},
  'LC': {name : 'Saint Lucia', code: 'LC', flag: countryCodeToFlag('LC')},
  'MF': {name : 'Saint Martin (French part)', code: 'MF', flag: countryCodeToFlag('MF')},
  'PM': {name : 'Saint Pierre and Miquelon', code: 'PM', flag: countryCodeToFlag('PM')},
  'VC': {name : 'Saint Vincent and the Grenadines', code: 'VC', flag: countryCodeToFlag('VC')},
  'WS': {name : 'Samoa', code: 'WS', flag: countryCodeToFlag('WS')},
  'SM': {name : 'San Marino', code: 'SM', flag: countryCodeToFlag('SM')},
  'ST': {name : 'Sao Tome and Principe', code: 'ST', flag: countryCodeToFlag('ST')},
  'SA': {name : 'Saudi Arabia', code: 'SA', flag: countryCodeToFlag('SA')},
  'SN': {name : 'Senegal', code: 'SN', flag: countryCodeToFlag('SN')},
  'RS': {name : 'Serbia', code: 'RS', flag: countryCodeToFlag('RS')},
  'SC': {name : 'Seychelles', code: 'SC', flag: countryCodeToFlag('SC')},
  'SL': {name : 'Sierra Leone', code: 'SL', flag: countryCodeToFlag('SL')},
  'SG': {name : 'Singapore', code: 'SG', flag: countryCodeToFlag('SG')},
  'SX': {name : 'Sint Maarten (Dutch part)', code: 'SX', flag: countryCodeToFlag('SX')},
  'SK': {name : 'Slovakia', code: 'SK', flag: countryCodeToFlag('SK')},
  'SI': {name : 'Slovenia', code: 'SI', flag: countryCodeToFlag('SI')},
  'SB': {name : 'Solomon Islands', code: 'SB', flag: countryCodeToFlag('SB')},
  'SO': {name : 'Somalia', code: 'SO', flag: countryCodeToFlag('SO')},
  'ZA': {name : 'South Africa', code: 'ZA', flag: countryCodeToFlag('ZA')},
  'GS': {name : 'South Georgia and the South Sandwich Islands', code: 'GS', flag: countryCodeToFlag('GS')},
  'SS': {name : 'South Sudan', code: 'SS', flag: countryCodeToFlag('SS')},
  'ES': {name : 'Spain', code: 'ES', flag: countryCodeToFlag('ES')},
  'LK': {name : 'Sri Lanka', code: 'LK', flag: countryCodeToFlag('LK')},
  'SD': {name : 'Sudan (the)', code: 'SD', flag: countryCodeToFlag('SD')},
  'SR': {name : 'Suriname', code: 'SR', flag: countryCodeToFlag('SR')},
  'SJ': {name : 'Svalbard and Jan Mayen', code: 'SJ', flag: countryCodeToFlag('SJ')},
  'SE': {name : 'Sweden', code: 'SE', flag: countryCodeToFlag('SE')},
  'CH': {name : 'Switzerland', code: 'CH', flag: countryCodeToFlag('CH')},
  'SY': {name : 'Syrian Arab Republic', code: 'SY', flag: countryCodeToFlag('SY')},
  'TW': {name : 'Taiwan (Province of China)', code: 'TW', flag: countryCodeToFlag('TW')},
  'TJ': {name : 'Tajikistan', code: 'TJ', flag: countryCodeToFlag('TJ')},
  'TZ': {name : 'Tanzania, United Republic of', code: 'TZ', flag: countryCodeToFlag('TZ')},
  'TH': {name : 'Thailand', code: 'TH', flag: countryCodeToFlag('TH')},
  'TL': {name : 'Timor-Leste', code: 'TL', flag: countryCodeToFlag('TL')},
  'TG': {name : 'Togo', code: 'TG', flag: countryCodeToFlag('TG')},
  'TK': {name : 'Tokelau', code: 'TK', flag: countryCodeToFlag('TK')},
  'TO': {name : 'Tonga', code: 'TO', flag: countryCodeToFlag('TO')},
  'TT': {name : 'Trinidad and Tobago', code: 'TT', flag: countryCodeToFlag('TT')},
  'TN': {name : 'Tunisia', code: 'TN', flag: countryCodeToFlag('TN')},
  'TR': {name : 'Turkey', code: 'TR', flag: countryCodeToFlag('TR')},
  'TM': {name : 'Turkmenistan', code: 'TM', flag: countryCodeToFlag('TM')},
  'TC': {name : 'Turks and Caicos Islands (the)', code: 'TC', flag: countryCodeToFlag('TC')},
  'TV': {name : 'Tuvalu', code: 'TV', flag: countryCodeToFlag('TV')},
  'UG': {name : 'Uganda', code: 'UG', flag: countryCodeToFlag('UG')},
  'UA': {name : 'Ukraine', code: 'UA', flag: countryCodeToFlag('UA')},
  'AE': {name : 'United Arab Emirates (the)', code: 'AE', flag: countryCodeToFlag('AE')},
  'GB': {name : 'United Kingdom of Great Britain and Northern Ireland (the)', code: 'GB', flag: countryCodeToFlag('GB')},
  'UK': {name : 'United Kingdom of Great Britain (the)', code: 'UK', flag: countryCodeToFlag('GB')},
  'UM': {name : 'United States Minor Outlying Islands (the)', code: 'UM', flag: countryCodeToFlag('UM')},
  'US': {name : 'United States of America (the)', code: 'US', flag: countryCodeToFlag('US')},
  'UY': {name : 'Uruguay', code: 'UY', flag: countryCodeToFlag('UY')},
  'UZ': {name : 'Uzbekistan', code: 'UZ', flag: countryCodeToFlag('UZ')},
  'VU': {name : 'Vanuatu', code: 'VU', flag: countryCodeToFlag('VU')},
  'VE': {name : 'Venezuela (Bolivarian Republic of)', code: 'VE', flag: countryCodeToFlag('VE')},
  'VN': {name : 'Viet Nam', code: 'VN', flag: countryCodeToFlag('VN')},
  'VG': {name : 'Virgin Islands (British)', code: 'VG', flag: countryCodeToFlag('VG')},
  'VI': {name : 'Virgin Islands (U.S.)', code: 'VI', flag: countryCodeToFlag('VI')},
  'WF': {name : 'Wallis and Futuna', code: 'WF', flag: countryCodeToFlag('WF')},
  'EH': {name : 'Western Sahara', code: 'EH', flag: countryCodeToFlag('EH')},
  'YE': {name : 'Yemen', code: 'YE', flag: countryCodeToFlag('YE')},
  'ZM': {name : 'Zambia', code: 'ZM', flag: countryCodeToFlag('ZM')},
  'ZW': {name : 'Zimbabwe', code: 'ZW', flag: countryCodeToFlag('ZW')},
  'AX': {name : 'Åland Islands', code: 'AX', flag: countryCodeToFlag('AX')},
  'EU': {name : 'European Union', code: 'EU', flag: countryCodeToFlag('EU')},
}

export function getCountry(countryCode: string): Country {
  const defaultCountry: Country = {name: 'Unknown Country', code: "XX", flag: '🏳️'}
  if (!countryCode || typeof countryCode !== 'string') {
    console.warn('Invalid country code provided, returning default country.');
    return defaultCountry;
  }

  const country = COUNTRY_MAPPING[countryCode.toUpperCase()];
  if (!country) {
    console.warn(`Country code "${countryCode}" not found in mapping.`);
    return defaultCountry;
  }
  return country;
}
