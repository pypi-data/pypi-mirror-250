from pyqcm import *
# set_global_parameter("nosym")
new_cluster_model('2x2_8b_C2v', 4, 8, generators=[[2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11], [3, 4, 1, 2, 7, 8, 5, 6, 11, 12, 9, 10]], bath_irrep=False)
new_cluster_operator('2x2_8b_C2v', 'tb1', 'one-body', [(1, 5, -1.0), (2, 6, -1.0), (3, 7, -1.0), (4, 8, -1.0), (13, 17, -1.0), (14, 18, -1.0), (15, 19, -1.0), (16, 20, -1.0)])
new_cluster_operator('2x2_8b_C2v', 'tb2', 'one-body', [(1, 9, -1.0), (2, 10, -1.0), (3, 11, -1.0), (4, 12, -1.0), (13, 21, -1.0), (14, 22, -1.0), (15, 23, -1.0), (16, 24, -1.0)])
new_cluster_operator('2x2_8b_C2v', 'eb1', 'one-body', [(5, 5, 1.0), (6, 6, 1.0), (7, 7, 1.0), (8, 8, 1.0), (17, 17, 1.0), (18, 18, 1.0), (19, 19, 1.0), (20, 20, 1.0)])
new_cluster_operator('2x2_8b_C2v', 'eb2', 'one-body', [(9, 9, 1.0), (10, 10, 1.0), (11, 11, 1.0), (12, 12, 1.0), (21, 21, 1.0), (22, 22, 1.0), (23, 23, 1.0), (24, 24, 1.0)])
new_cluster_operator('2x2_8b_C2v', 'ds1', 'anomalous', [(5, 18, -1.0), (6, 17, -1.0), (7, 20, -1.0), (8, 19, -1.0), (5, 19, 1.0), (7, 17, 1.0), (6, 20, 1.0), (8, 18, 1.0)])
new_cluster_operator('2x2_8b_C2v', 'ds2', 'anomalous', [(9, 22, -1.0), (10, 21, -1.0), (11, 24, -1.0), (12, 23, -1.0), (9, 23, 1.0), (11, 21, 1.0), (10, 24, 1.0), (12, 22, 1.0)])
add_cluster('2x2_8b_C2v', [0, 0, 0], [[0, 0, 0], ( 1, 0, 0), ( 0, 1, 0), ( 1, 1, 0)], ref = 0)
lattice_model('2x2_8b_C2v', [( 2, 0, 0), ( 0, 2, 0)], None)
interaction_operator('U')
hopping_operator('t', ( 1, 0, 0), -1)
hopping_operator('t', ( 0, 1, 0), -1)
hopping_operator('tp', ( 1, 1, 0), -1)
hopping_operator('tp', [1, -1, 0], -1)
hopping_operator('tpp', ( 2, 0, 0), -1)
hopping_operator('tpp', ( 0, 2, 0), -1)
anomalous_operator('D', ( 1, 0, 0), 1)
anomalous_operator('D', ( 0, 1, 0), -1)
anomalous_operator('extS', ( 1, 0, 0), 1)
anomalous_operator('extS', ( 0, 1, 0), 1)
anomalous_operator('S', [0, 0, 0], 1)

try:
    import model_extra
except:
    pass		
set_target_sectors(['R0:N12:S0'])
set_parameters("""

    U=8.0
    mu=4
    t=1
    tb1_1=0.5
    tb2_1=0.5
    eb1_1=0.5
    eb2_1=-0.5
""")
set_parameter("U", 8.0)
set_parameter("eb1_1", 2.0485227015084444)
set_parameter("eb2_1", -2.050573220609422)
set_parameter("mu", 4.0)
set_parameter("t", 1.0)
set_parameter("tb1_1", 0.7380717307031983)
set_parameter("tb2_1", 0.738411885659026)

new_model_instance(0)

solution=[None]*1

#--------------------- cluster no 1 -----------------
solution[0] = """
U	8
eb1	2.04852
eb2	-2.05057
mu	4
t	1
tb1	0.738072
tb2	0.738412

GS_energy: -34.4851 GS_sector: R0:N12:S0:1
GF_format: bl
mixing	0
state
R0:N12:S0	-34.4851	1
w	1	39
-1.740405346525	0.34805002573958
-2.3745880724041	0.20536461385885
-2.8463472206476	-0.23112130858853
-4.6368497010927	0.7465269654096
-5.339661479358	-0.079485167651562
-5.7168015643926	0.096158773861842
-6.1527129479121	0.04312080338348
-7.245700110134	-0.017552963051718
-8.1581924906494	-0.027534409162202
-9.3828183956501	-0.024868058341087
-10.078428238414	-0.036116786642604
-11.289641216421	-0.012371693573916
-12.516144758812	0.017707306486957
-13.803782187917	-0.0060926386886993
-15.212054236092	-0.0030394470183243
-16.392819353779	-0.0029223300382836
-18.073794743297	0.00042343335943232
-19.996078061916	0.00020667433047235
2.0250714486914	0.025268879871794
2.2374304516017	0.15069027626967
2.9247867118738	-0.041034889967057
5.2877523915601	-0.015682169416396
5.5050031400729	-0.078074503904368
5.7885446502896	-0.10733418480491
6.1154825274275	0.27180998267523
6.3100849425061	-0.29115764079921
7.0391612028233	0.017789853727471
8.1543710060605	0.024981184326613
8.6893495865948	0.026637917303962
9.7327017560292	0.028211935876088
10.611978227897	-0.017339923689564
11.64335406833	0.015393371525328
12.487925701447	-0.018811353347026
13.699439964389	0.010104755377364
14.772461773341	-0.0063132298892911
15.427426054886	0.0026304545205699
17.049226010984	-0.00052109921254245
18.522903285547	0.00025206399633946
19.974150390042	-0.00019361822725572
w	1	45
-1.5450120168976	-0.37282851708081
-2.2418883542368	0.20846489996687
-2.4880965162565	0.0093354394426413
-2.863169851937	0.12812393871846
-2.9486378597418	0.012093477557945
-4.0254220596386	-0.45185628919165
-4.8817864360356	-0.027515933965565
-5.5676465585149	-0.051897151591034
-6.2862779276314	0.089727153228176
-6.8022370863873	0.2825392223549
-7.3420756890248	-0.044606622687265
-8.3788485254776	-0.037462832771833
-9.5434334412429	0.024911723540736
-10.267742787018	0.026733331496273
-11.342528442126	-0.015283193692015
-12.393201211774	0.018826871864943
-13.596734472413	0.0065962638285597
-14.588145311906	0.0047364916604331
-15.9556118385	0.0013771567977749
-17.06936977028	0.0019898830869073
-18.458834777521	0.00035874733093185
-20.14824237415	0.000157420339214
1.5439864931135	0.37252783832743
2.2398817804245	0.20854220148767
2.4860183552633	-0.0095330109503865
2.8610396124826	-0.12794796286691
2.9370783145203	-0.013590248291373
4.024246556844	0.45205103553622
4.8749368675713	0.027199779913294
5.5475346480876	0.050502172607926
6.2259840140701	-0.080695405275972
6.781209022664	-0.27634487784004
7.074881047795	-0.083666830053365
8.2683216853695	-0.037632299157783
9.1470221715372	0.021684212303224
10.047340194624	0.030201806879368
11.034388690562	0.017139159834701
12.254149967561	0.018867245909661
13.030392464323	0.0086665352718102
14.231917592678	-0.0058344524460025
15.223030213551	-0.0023950873135086
16.952936436739	-0.0020590246537992
17.835778972313	-0.00061676296252394
19.391011270965	0.00019414381215996
20.773282918791	-0.00013167129392241
w	1	44
-1.5450120168976	-0.37282851708083
-2.2418883544509	0.20846490037774
-2.4880988025575	0.0093355140093927
-2.863170417552	0.12812472836108
-2.9486977501839	0.012085059069965
-4.0254220656746	-0.45185629318685
-4.8818152927652	-0.027517502191788
-5.5677248849225	-0.051902870408852
-6.2864955049292	0.08976076712561
-6.8022909067564	0.28254076579975
-7.3432351379008	-0.044530270448617
-8.3792766342576	-0.037458395449666
-9.5448474672609	0.024936201424447
-10.26898624828	0.026710858276066
-11.344135813576	0.015276269075074
-12.393719401228	-0.018822524215213
-13.598819047489	-0.0065942906713552
-14.589795378563	0.0047303027511817
-15.960353273331	0.0013752078651024
-17.070047506328	0.0019887957164076
-18.461707277194	-0.00035800975985588
-20.151696128773	0.00015736416926303
1.5439864931139	0.3725278383284
2.2398818129095	-0.20854226413342
2.4863599276374	-0.009544605019069
2.8611398967944	-0.128097790528
2.946570406087	0.012088995809939
4.0242476230459	-0.45205177743699
4.8808166221715	0.027533694343796
5.5657816941738	0.051930596651195
6.2848429230175	-0.089549145020901
6.8018631829131	-0.28262309135348
7.34225032765	0.044567797964716
8.3778811548614	0.037475292948357
9.5428796632063	-0.024905725489617
10.267400168906	0.026740934880339
11.342476909377	-0.015277362008672
12.393130461047	-0.018829689224311
13.596459304932	0.0065996368718727
14.587687762209	-0.0047371561074346
15.957772902839	0.0013756784576657
17.069097783669	-0.0019901024120453
18.45970997239	-0.0003584965250819
20.149630127766	0.00015742568578308
w	1	39
-2.0269205166061	0.02545900497857
-2.2394197849242	0.15073290079207
-2.926847178804	-0.041058907534688
-5.2929440918993	-0.016263002526325
-5.5091674920065	0.078800210833198
-5.7963483057519	0.10904873890882
-6.119898008598	-0.27474824324663
-6.3128505294633	0.2875030400357
-7.0572455299528	-0.017421414786741
-8.165491775896	-0.025281683688648
-8.7009097345773	-0.026351100999531
-9.7380942012901	-0.028232718138485
-10.624676827393	0.017284808845218
-11.657293405831	0.015413785153638
-12.493986057156	0.0187355816146
-13.707730063057	0.010090741403622
-14.790675460577	-0.0063329770072703
-15.465408166736	0.0024528020714653
-17.084522415142	0.00051094013956084
-18.559680426112	0.00024857209396508
-19.999569775903	-0.00019290785051615
1.7389141091941	0.34769237306385
2.3725494883306	0.20532625112031
2.8443456882678	-0.23107907138399
4.6361324087002	-0.74667417992908
5.3378802888976	0.079720795065243
5.7149988798108	0.096315646313075
6.1519032321344	-0.043054086704067
7.246678081434	0.017565823691635
8.1575892881505	0.027540235187617
9.3845303228322	-0.02491457427132
10.079296378817	-0.036084872438072
11.293125786036	0.012355380872881
12.516953755141	0.017708315531227
13.80620021356	0.0060847795829744
15.215877481456	-0.0030340948245204
16.393061057954	-0.0029211070267091
18.078621528111	-0.00042203692976881
20.000010812914	0.00020658183162807

"""
read_cluster_model_instance(solution[0], 0)
