class remoteDictionary:
	def __init__(self):
		self.Remote2StopID = {}
		self.Remote2StopID['DITMARS BL-31 S,NQ'] = 'R01' #Astoria - Ditmars BLVD
		self.Remote2StopID['HOYT ST-ASTORIA,NQ'] = 'R03' #Astoria BLVD
		self.Remote2StopID['GRAND-30 AVE,NQ'] = 'R04' #30 AV
		self.Remote2StopID['BROADWAY-31 ST,NQ'] = 'R05' #BROADWAY
		self.Remote2StopID['WASHINGTON-36 A,NQ'] = 'R06' #36 AV
		self.Remote2StopID['BEEBE-39 AVE,NQ'] = 'R08' #39 AV
		self.Remote2StopID['LEXINGTON AVE,456NQR'] = 'R11' #Lexington AV/59 ST
		self.Remote2StopID['5 AVE-59 ST,NQR'] = 'R13' #5 AV/59 ST
		self.Remote2StopID['57 ST-7 AVE,NQR'] = 'R14' #57 ST- 7AV
		self.Remote2StopID['49 ST-7 AVE,NQR'] = 'R15' #49 ST
		self.Remote2StopID['42 ST-TIMES SQ,1237ACENQRS'] = 'R16' #TIMES SQ 42 ST
		self.Remote2StopID['34 ST-HERALD SQ,BDFMNQR'] = 'R17' #34 ST Herald Sq
		self.Remote2StopID['28 ST-BROADWAY,NR'] = 'R18' #28 ST
		self.Remote2StopID['23 ST-5 AVE,NR'] = 'R19'
		self.Remote2StopID['14 ST-UNION SQ,LNQR456'] = 'R20'
		self.Remote2StopID["8 ST-B'WAY NYU,NR"] = 'R21'
		self.Remote2StopID["PRINCE ST-B'WAY,NR"] = 'R22'
		self.Remote2StopID['CANAL ST,JNQRZ6'] = 'R23'
		#self.Remote2StopID['BOROUGH HALL/CT'] = 'R24'
		self.Remote2StopID['CORTLANDT ST,R'] = 'R25'
		self.Remote2StopID['RECTOR ST,R'] = 'R26'
		self.Remote2StopID['WHITEHALL ST,R1'] = 'R27'
		self.Remote2StopID['BOROUGH HALL/CT,2345R'] = 'R28'
		self.Remote2StopID['JAY ST-METROTEC,R'] = 'R29'
		self.Remote2StopID['DEKALB AVE,BDNQR'] = 'R30'
		self.Remote2StopID['ATLANTIC AVE,2345BDNQR'] = 'R31'
		self.Remote2StopID['UNION ST,R'] = 'R32'
		self.Remote2StopID['9 ST,DFGMNR'] = 'R33'
		self.Remote2StopID['PROSPECT AVE,R'] = 'R34'
		self.Remote2StopID['25 ST,R'] = 'R35'
		self.Remote2StopID['36 ST,DNR'] = 'R36'
		self.Remote2StopID['45 ST,R'] = 'R39'
		self.Remote2StopID['53 ST,R'] = 'R40'
		self.Remote2StopID['59 ST,NR'] = 'R41'
		self.Remote2StopID['BAY RIDGE AVE,R'] = 'R42'
		self.Remote2StopID['77 ST,R'] = 'R43'
		self.Remote2StopID['86 ST,R'] = 'R44'
		self.Remote2StopID['BAY RIDGE-95 ST,R'] = 'R45'
		self.Remote2StopID['ATLANTIC AVE,2345BDNQR'] = 'D24'
		self.Remote2StopID['7 AVE,BQ'] = 'D25'
		self.Remote2StopID['PROSPECT PARK,BQS'] = 'D26'
		self.Remote2StopID['PARKSIDE AVE,BQ'] = 'D27'
		self.Remote2StopID['CHURCH AVE,BQ'] = 'D28'
		self.Remote2StopID['BEVERLEY ROAD,BQ'] = 'D29'
		self.Remote2StopID['CORTELYOU ROAD,BQ'] = 'D30'
		self.Remote2StopID['NEWKIRK AVE,BQ'] = 'D31'
		self.Remote2StopID['AVE H,BQ'] = 'D32'
		self.Remote2StopID['AVE J,BQ'] = 'D33'
		self.Remote2StopID['AVE M,BQ'] = 'D34'
		self.Remote2StopID['KINGS HIGHWAY,BQ'] = 'D35'
		self.Remote2StopID['AVE U,BQ'] = 'D37'
		self.Remote2StopID['NECK ROAD,BQ'] = 'D38'
		self.Remote2StopID['SHEEPSHEAD BAY,BQ'] = 'D39'
		self.Remote2StopID['BRIGHTON BEACH,BQ'] = 'D40'
		self.Remote2StopID['OCEAN PARKWAY,Q'] = 'D41'
		self.Remote2StopID['W 8 ST-AQUARIUM,FQ'] = 'D42'
		self.Remote2StopID['STILLWELL AVE,DFNQ'] = 'D43'
		self.Remote2StopID['9 AVE,D'] = 'B12'
		self.Remote2StopID['FT HAMILTON PKY,D'] = 'B13'
		self.Remote2StopID['BAY 50 ST,D'] = 'B14'
		self.Remote2StopID['55 ST,D'] = 'B15'
		#self.Remote2StopID['AVE H'] = 'B16'
		self.Remote2StopID['71 ST,D'] = 'B17'
		self.Remote2StopID['79 ST,D'] = 'B18'
		self.Remote2StopID['18 AVE,D'] = 'B19'
		self.Remote2StopID['20 AVE,D'] = 'B20'
		self.Remote2StopID['BAY PARKWAY,D'] = 'B21'
		self.Remote2StopID['25 AVE,D'] = 'B22'
		self.Remote2StopID['BAY 50 ST,D'] = 'B23'
		self.Remote2StopID['8 AVE,N'] = 'N02'
		self.Remote2StopID['FT HAMILTON PKY,N'] = 'N03'
		self.Remote2StopID['NEW UTRECHT AVE,ND'] = 'N04'
		self.Remote2StopID['18 AVE,N'] = 'N05'
		self.Remote2StopID['20 AVE,N'] = 'N06'
		self.Remote2StopID['BAY PKY-22 AVE,N'] = 'N07'
		self.Remote2StopID['KINGS HIGHWAY,N'] = 'N08'
		self.Remote2StopID['AVE U,N'] = 'N09'
		self.Remote2StopID['86 ST,N'] = 'N10'
		self.Remote2StopID['121 ST,JZ'] = 'J12'
		self.Remote2StopID['111 ST,J'] = 'J13'
		self.Remote2StopID['104 ST,JZ'] = 'J14'
		self.Remote2StopID['WOODHAVEN BLVD,JZ'] = 'J15'
		self.Remote2StopID['FOREST PARKWAY,J'] = 'J16'
		self.Remote2StopID['ELDERTS LANE,JZ'] = 'J17'
		self.Remote2StopID['CYPRESS HILLS,J'] = 'J19'
		self.Remote2StopID['CRESCENT ST,JZ'] = 'J20'
		self.Remote2StopID['NORWOOD AVE,JZ'] = 'J21'
		self.Remote2StopID['CLEVELAND ST,J'] = 'J22'
		self.Remote2StopID['VAN SICLEN AVE,JZ'] = 'J23'
		self.Remote2StopID['ALABAMA AVE,J'] = 'J24'
		self.Remote2StopID['BROADWAY-ENY,ACJLZ'] = 'J27'
		self.Remote2StopID['CHAUNCEY ST,JZ'] = 'J28'
		self.Remote2StopID['HALSEY ST,J'] = 'J29'
		self.Remote2StopID['GATES AVE,JZ'] = 'J30'
		self.Remote2StopID['KOSCIUSZKO ST,J'] = 'J31'
		self.Remote2StopID['MYRTLE AVE,JMZ'] = 'M11'
		self.Remote2StopID['FLUSHING AVE,JM'] = 'M12'
		self.Remote2StopID['LORIMER ST,JM'] = 'M13'
		self.Remote2StopID['HEWES ST,JM'] = 'M14'
		self.Remote2StopID['MARCY AVE,JMZ'] = 'M16'
		self.Remote2StopID['ESSEX ST,FJMZ'] = 'M18'
		self.Remote2StopID['BOWERY,JZ'] = 'M19'
		self.Remote2StopID['CANAL ST,JNQRZ6'] = 'M20'
		self.Remote2StopID['CHAMBERS ST,456JZ'] = 'M21'
		self.Remote2StopID['FULTON ST,ACJZ2345'] = 'M22'
		self.Remote2StopID['BROAD ST,JZ'] = 'M23'
		self.Remote2StopID['METROPOLITAN AV,M'] = 'M01'
		self.Remote2StopID['FRESH POND ROAD,M'] = 'M04'
		self.Remote2StopID['FOREST AVE,M'] = 'M05'
		self.Remote2StopID['SENECA AVE,M'] = 'M06'
		self.Remote2StopID['MYRTLE AVE,LM'] = 'M08'
		self.Remote2StopID['KNICKERBOCKER,M'] = 'M09'
		self.Remote2StopID['CENTRAL AVE,M'] = 'M10'
		self.Remote2StopID['8 AVE,ACEL'] = 'L01'
		self.Remote2StopID['14 ST-6 AVE,FLM123'] = 'L02'
		self.Remote2StopID['6 AVE,FLM123'] = 'L02'
		self.Remote2StopID['14 ST-UNION SQ,LNQR456'] = 'L03'
		self.Remote2StopID['3 AVE,L'] = 'L05'
		self.Remote2StopID['1 AVE,L'] = 'L06'
		self.Remote2StopID['BEDFORD AVE,L'] = 'L08'
		self.Remote2StopID['LORIMER ST,GL'] = 'L10'
		self.Remote2StopID['GRAHAM AVE,L'] = 'L11'
		self.Remote2StopID['GRAND ST,L'] = 'L12'
		self.Remote2StopID['MONTROSE AVE,L'] = 'L13'
		self.Remote2StopID['MORGAN AVE,L'] = 'L14'
		self.Remote2StopID['JEFFERSON ST,L'] = 'L15'
		self.Remote2StopID['DEKALB AVE,L'] = 'L16'
		self.Remote2StopID['MYRTLE AVE,LM'] = 'L17'
		self.Remote2StopID['HALSEY ST,L'] = 'L19'
		self.Remote2StopID['WILSON AVE,L'] = 'L20'
		self.Remote2StopID['BUSHWICK AVE,L'] = 'L21'
		self.Remote2StopID['BROADWAY-ENY,ACJLZ'] = 'L22'
		self.Remote2StopID['ATLANTIC AVE,L'] = 'L24'
		self.Remote2StopID['SUTTER AVE,L'] = 'L25'
		self.Remote2StopID['LIVONIA AVE,L'] = 'L26'
		self.Remote2StopID['NEW LOTS AVE,L'] = 'L27'
		self.Remote2StopID['EAST 105 ST,L'] = 'L28'
		self.Remote2StopID['ROCKAWAY PKY,L'] = 'L29'
		self.Remote2StopID['FRANKLIN AVE,ACS'] = 'S01'
		self.Remote2StopID['BOTANIC GARDEN,S2345'] = 'S04'
		self.Remote2StopID['PARK PLACE,S'] = 'S03'
		self.Remote2StopID['INWOOD-207 ST,A'] = 'A02'
		self.Remote2StopID['DYCKMAN-200 ST,A'] = 'A03'
		self.Remote2StopID['190 ST,A'] = 'A05'
		self.Remote2StopID['181 ST,A'] = 'A06'
		self.Remote2StopID['175 ST,A'] = 'A07'
		self.Remote2StopID['168 ST-BROADWAY,1AC'] = 'A09'
		self.Remote2StopID['163 ST-AMSTERDM,C'] = 'A10'
		self.Remote2StopID['155 ST,C'] = 'A11'
		self.Remote2StopID['145 ST,ABCD'] = 'A12'
		self.Remote2StopID['135 ST,BC'] = 'A14'
		self.Remote2StopID['125 ST,ABCD'] = 'A15'
		self.Remote2StopID['116 ST,BC'] = 'A16'
		self.Remote2StopID['CATHEDRL-110 ST,BC'] = 'A17'
		self.Remote2StopID['103 ST,BC'] = 'A18'
		self.Remote2StopID['96 ST,BC'] = 'A19'
		self.Remote2StopID['86 ST,BC'] = 'A20'
		self.Remote2StopID['81 ST-MUSEUM,BC'] = 'A21'
		self.Remote2StopID['72 ST,BC'] = 'A22'
		self.Remote2StopID['59 ST-COLUMBUS,1ABCD'] = 'A24'
		self.Remote2StopID['50 ST,CE'] = 'A25'
		self.Remote2StopID['42 ST-PA BUS TE,ACENQRS1237'] = 'A27'
		self.Remote2StopID['34 ST-PENN STA,123ACE'] = 'A28'
		self.Remote2StopID['23 ST,CE'] = 'A30'
		self.Remote2StopID['14 ST,ACEL'] = 'A31'
		self.Remote2StopID['W 4 ST-WASH SQ,ABCDEFM'] = 'A32'
		#self.Remote2StopID['BOTANIC GARDEN'] = 'D20'
		self.Remote2StopID['SPRING ST,CE'] = 'A33'
		self.Remote2StopID['CANAL ST,ACE'] = 'A34'
		self.Remote2StopID['CHAMBERS ST,ACE23'] = 'A36'
		self.Remote2StopID['WORLD TRADE CTR,23ACE'] = 'E01'
		self.Remote2StopID['FULTON ST,2345ACJZ'] = 'A38'
		self.Remote2StopID['HIGH ST,AC'] = 'A40'
		self.Remote2StopID['JAY ST-METROTEC,ACF'] = 'A41'
		self.Remote2StopID['HOYT/SCHERMER,ACG'] = 'A42'
		self.Remote2StopID['LAFAYETTE AVE,C'] = 'A43'
		self.Remote2StopID['CLINTON-WASH AV,C'] = 'A44'
		self.Remote2StopID['FRANKLIN AVE,ACS'] = 'A45'
		self.Remote2StopID['NOSTRAND AVE,AC'] = 'A46'
		self.Remote2StopID['KINGSTON-THROOP,C'] = 'A47'
		self.Remote2StopID['UTICA AVE,AC'] = 'A48'
		self.Remote2StopID['RALPH AVE,C'] = 'A49'
		self.Remote2StopID['ROCKAWAY AVE,C'] = 'A50'
		self.Remote2StopID['BROADWAY-ENY,ACJLZ'] = 'A51'
		self.Remote2StopID['LIBERTY AVE,C'] = 'A52'
		self.Remote2StopID['VAN SICLEN AVE,C'] = 'A53'
		self.Remote2StopID['SHEPHERD AVE,C'] = 'A54'
		self.Remote2StopID['EUCLID AVE,AC'] = 'A55'
		self.Remote2StopID['GRANT AVE,A'] = 'A57'
		self.Remote2StopID['HUDSON-80 ST,A'] = 'A59'
		self.Remote2StopID['BOYD-88 ST,A'] = 'A60'
		self.Remote2StopID['ROCKAWAY BLVD,A'] = 'A61'
		self.Remote2StopID['OXFORD-104 ST,A'] = 'A63'
		self.Remote2StopID['GREENWOOD-111,A'] = 'A64'
		self.Remote2StopID['LEFFERTS BLVD,A'] = 'A65'
		self.Remote2StopID['AQUEDUCT TRACK,A'] = 'H01'
		self.Remote2StopID['AQUEDUCT-N CNDT,A'] = 'H02'
		self.Remote2StopID['HOWARD BCH-JFK,A'] = 'H03'
		self.Remote2StopID['BROAD CHANNEL,AS'] = 'H04'
		#self.Remote2StopID['BEACH 90 ST,AS'] = 'H19'
		self.Remote2StopID['BEACH 90 ST,AS'] = 'H12'
		self.Remote2StopID['BEACH 98 ST,AS'] = 'H13'
		self.Remote2StopID['BEACH 105 ST,AS'] = 'H14'
		self.Remote2StopID['ROCKAWAY PK 116,AS'] = 'H15'
		self.Remote2StopID['BEACH 67 ST,A'] = 'H06'
		self.Remote2StopID['BEACH 60 ST,A'] = 'H07'
		self.Remote2StopID['BEACH 44 ST,A'] = 'H08'
		self.Remote2StopID['BEACH 36 ST,A'] = 'H09'
		self.Remote2StopID['BEACH 25 ST,A'] = 'H10'
		self.Remote2StopID['FAR ROCKAWAY,A'] = 'H11'
		












































