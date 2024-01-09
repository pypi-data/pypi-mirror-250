from .SHARPPYMAIN.sharppy.sharptab.profile import create_profile
from .SHARPPYMAIN.sharppy.sharptab.interp import *
from .SHARPPYMAIN.sharppy.sharptab.winds import *
from .SHARPPYMAIN.sharppy.sharptab.utils import comp2vec 
from .SHARPPYMAIN.sharppy.sharptab.params import *


from ecape.calc import calc_ecape, _get_parcel_profile, calc_mse, calc_integral_arg, calc_lfc_height, calc_el_height

import numpy as np
import numpy.ma as ma
import warnings
import metpy.calc as mpcalc
from metpy.units import units



#########################################################
#            SOUNDERPY SPYCALC FUNCTIONS                #
# (C) KYLE J GILLETT, CENTRAL MICHIGAN UNIVERSTIY, 2023 #
#########################################################



class sounding_params:


    def __init__(self, clean_data, storm_motion='rm'):
            self.clean_data = clean_data 
            self.storm_motion = storm_motion

            
    ######################################################################################################
    ### CALC FUNCTION -- COMPUTE VALUES ###
    ######################################################################################################        
    def calc(self):
        
        def calculate_height(pressure, pressure_at_sea_level=1013.25):
            # Constants
            R = 287.05  # Specific gas constant for dry air in J/(kg K)
            T0 = 288.15  # Standard temperature at sea level in K
            g = 9.8  # Acceleration due to gravity in m/s^2
            # Calculate height using the hypsometric equation
            height = (R * T0 / g) * np.log(pressure_at_sea_level / pressure)
            return height
    
        def find_nearest(array, value):
            array = np.asarray(array)
            nearest_idx = (np.abs(array - value)).argmin()
            return nearest_idx
    
    

        general = {}
        kinem  = {} 
        thermo = {}
        intrp  = {}

        # declare easy variable names for reuse from `clean_data`
        # first, check for correct units: 
        if self.clean_data['T'].units != 'degree_Celsius':
            self.clean_data['T'] =  self.clean_data['T'].to(units.degC)
        if self.clean_data['Td'].units != 'degree_Celsius':
            self.clean_data['Td'] = self.clean_data['Td'].to(units.degC)
        
        T   = self.clean_data['T']
        Td  = self.clean_data['Td']
        p   = self.clean_data['p']
        z   = self.clean_data['z']
        u   = self.clean_data['u']
        v   = self.clean_data['v']
        wd  = mpcalc.wind_direction(u, v)
        ws  = mpcalc.wind_speed(u, v)

        # compute useful variables and add them to a new dict of 
        # data that this function will return 
        if self.clean_data['site_info']['site-elv'] == 9999:
            general['elevation'] = z[0].m
        else:
            general['elevation'] = int(self.clean_data['site_info']['site-elv'])


        general['sfc_pressure']  = (p[0].m*(1-(0.0065*(general['elevation']))/(T[0].m+(0.0065*(general['elevation']))+273.15))**-5.257)*units.hPa
        general['wet_bulb']      = mpcalc.wet_bulb_temperature(p, T, Td)
        general['rel_humidity']  = mpcalc.relative_humidity_from_dewpoint(T, Td)*100
        general['spec_humidity'] = (mpcalc.specific_humidity_from_dewpoint(p, Td)*1000)*units.g/units.kg
        general['mix_ratio']     = mpcalc.mixing_ratio_from_specific_humidity(general['spec_humidity'])
        general['virt_temp']     = mpcalc.virtual_temperature(T, general['mix_ratio'])
        general['theta']         = mpcalc.potential_temperature(p, T)
        general['theta_e']       = mpcalc.equivalent_potential_temperature(p, T, Td)
        try:
            general['pwat']      = mpcalc.precipitable_water(p, Td).to('in')
            if general['pwat'] < 0:
                general['pwat'] = ma.masked
        except:
            general['pwat'] = ma.masked
        # FREEZING POINT CALCULATION---           
        try: 
            frz_pt_index = T.m.tolist().index(list(filter(lambda i: i <= 0, T.m.tolist()))[0])
            general['frz_pt_p'] = p[frz_pt_index]
            general['frz_pt_z'] = z[frz_pt_index]
        except IndexError:
            general['frz_pt_p'] = ma.masked
            general['frz_pt_z'] = ma.masked
            warnings.warn("This sounding does not have a freezing point (not enough data)", Warning)
            pass
        ##########################################   



        def interpolate(var,hgts,step):
            levels=np.arange(0,np.max(hgts),step)
            varinterp=np.zeros(len(levels))
            for i in range(0,len(levels)):
                try:
                    lower=np.where(hgts-levels[i]<=0,hgts-levels[i],-np.inf).argmax()
                    varinterp[i]=(((var[lower+1]-var[lower])/(hgts[lower+1]-hgts[lower]))*(levels[i]-hgts[lower])+var[lower])
                except IndexError:
                    # Handle the case where the index is out of bounds
                    varinterp[i] = np.nan 
            return varinterp 

        resolution=100

        rhINTRP = general['rel_humidity'].m[np.isnan(z)==False]
        mrINTRP = general['mix_ratio'].m[np.isnan(z)==False]
        thetaINTRP  = general['theta'].m[np.isnan(z)==False]
        thetaeINTRP = general['theta_e'].m[np.isnan(z)==False]
        pINTRP  = p.m[np.isnan(z)==False]
        uINTRP  = u.m[np.isnan(z)==False]
        vINTRP  = v.m[np.isnan(z)==False]
        zINTRP  = z.m[np.isnan(z)==False]
        zINTRP  = zINTRP-zINTRP[0]
        # Interpolation, add to intrp dict
        intrp['rhINTRP'] = interpolate(rhINTRP,zINTRP,resolution)
        intrp['mrINTRP'] = interpolate(mrINTRP,zINTRP,resolution)
        intrp['thetaINTRP']  = interpolate(thetaINTRP,zINTRP,resolution)
        intrp['thetaeINTRP'] = interpolate(thetaeINTRP,zINTRP,resolution)
        intrp['pINTRP'] = interpolate(pINTRP,zINTRP,resolution)
        intrp['uINTRP'] = interpolate(uINTRP,zINTRP,resolution)
        intrp['vINTRP'] = interpolate(vINTRP,zINTRP,resolution)
        intrp['zINTRP'] = interpolate(zINTRP,zINTRP,resolution)

        hgt_lvls = {}
        hgt_var_list = ['h0', 'h05', 'h1', 'h15', 'h2', 'h25', 
                        'h3', 'h35', 'h4', 'h45', 'h5', 'h55', 
                        'h6', 'h65', 'h7', 'h75', 'h8', 'h85', 
                        'h9', 'h10', 'h11', 'h12', 'h13', 'h14']
        hgt_val_list = [0.,500.,1000.,1500.,2000.,2500.,3000.,3500.,
                        4000.,4500.,5000.,5500.,6000.,6500.,7000.,
                        7500.,8000.,8500.,9000.,10000.,11000.,
                        12000.,13000.,14000.]

        for var, val, in zip(hgt_var_list, hgt_val_list):
            try:
                hgt_lvls[var] = np.where(intrp['zINTRP']==val)[0][0]
            except:
                pass
        intrp['hgt_lvls'] = hgt_lvls


        ###################################################################
        ### SHARPPY VARIABLES CALC ###
        ###################################################################
        # create sharppy profile object
        prof = create_profile(profile='default',pres=p.m, hght=z.m, tmpc=T.m, dwpc=Td.m, wspd=ws, wdir=wd, 
                                      missing=-9999, strictQC=False)

        ####################################################################
        ### THERMODYNAMIC VALUES ###
        ####################################################################
        #--- SURFACE BASED PARCEL PROPERTIES ---#
        # ---------------------------------------------------------------
        sbpcl = parcelx(prof, flag=1, pres=p[0].m, tmpc=T[0].m, dwpc=Td[0].m)
        thermo['sbT_trace'] = sbpcl.ttrace
        thermo['sbP_trace'] = sbpcl.ptrace
        thermo['sbZ_trace'] = general['elevation'] + calculate_height(thermo['sbP_trace'])
        # compute heights
        thermo['sb_lcl_p'] = sbpcl.lclpres
        thermo['sb_lcl_z'] = sbpcl.lclhght 
        thermo['sb_lfc_p'] = sbpcl.lfcpres
        thermo['sb_lfc_z'] = sbpcl.lfchght
        thermo['sb_el_p']  = sbpcl.elpres  
        thermo['sb_el_z']  = sbpcl.elhght
        thermo['sb_el_T']  = temp(prof, pres(prof, thermo['sb_el_z']))
        thermo['sbcape']   = sbpcl.bplus
        thermo['sbcin']    = sbpcl.bminus
        thermo['sb3cape']  = sbpcl.b3km
        thermo['sb6cape']  = sbpcl.b6km

        #--- MOST UNSTABLE PARCEL PROPERTIES ---#
        # ---------------------------------------------------------------
        mupcl_p, mupcl_T, mupcl_Td = mpcalc.most_unstable_parcel(p, T, Td)[0:3]
        mupcl = parcelx(prof, flag=3, pres=mupcl_p.m, tmpc=mupcl_T.m, dwpc=mupcl_Td.m)
        thermo['muT_trace'] = mupcl.ttrace
        thermo['muP_trace'] = mupcl.ptrace
        thermo['muZ_trace'] = general['elevation'] + calculate_height(thermo['muP_trace'])
        # compute heights
        thermo['mu_lcl_p'] = mupcl.lclpres 
        thermo['mu_lcl_z'] = mupcl.lclhght 
        thermo['mu_lfc_p'] = mupcl.lfcpres 
        thermo['mu_lfc_z'] = mupcl.lfchght
        thermo['mu_el_p']  = mupcl.elpres
        thermo['mu_el_z']  = mupcl.elhght
        thermo['mu_el_T']  = temp(prof, pres(prof, thermo['mu_el_z']))
        thermo['mucape']   = mupcl.bplus
        thermo['mucin']    = mupcl.bminus
        thermo['mu3cape']  = mupcl.b3km
        thermo['mu6cape']  = mupcl.b6km

        #--- MIXED LAYER PARCEL PROPERTIES ---#
        # ---------------------------------------------------------------
        mlpcl_p, mlpcl_T, mlpcl_Td = mpcalc.mixed_parcel(p, T, Td, interpolate=True)[0:3]
        mlpcl = parcelx(prof, flag=5, pres=mlpcl_p.m, tmpc=mlpcl_T.m, dwpc=mlpcl_Td.m)
        thermo['mlT_trace'] = mlpcl.ttrace
        thermo['mlP_trace'] = mlpcl.ptrace
        # compute heights
        thermo['ml_lcl_p'] = mlpcl.lclpres
        thermo['ml_lcl_z'] = mlpcl.lclhght
        thermo['ml_lfc_p'] = mlpcl.lfcpres
        thermo['ml_lfc_z'] = mlpcl.lfchght
        thermo['ml_el_p']  = mlpcl.elpres
        thermo['ml_el_z']  = mlpcl.elhght
        thermo['ml_el_T']  = temp(prof, pres(prof, thermo['ml_el_z']))
        thermo['mlcape']   = mlpcl.bplus
        thermo['mlcin']    = mlpcl.bminus
        thermo['ml3cape']  = mlpcl.b3km
        thermo['ml6cape']  = mlpcl.b6km

        #--- NORMALIZED CAPE ---#
        # ---------------------------------------------------------------
        thermo['mu_ncape'] = np.round(thermo['mucape'] / ((thermo['mu_el_z'] - thermo['mu_lfc_z'])),1)
        thermo['sb_ncape'] = np.round(thermo['sbcape'] / ((thermo['sb_el_z'] - thermo['sb_lfc_z'])),1)
        thermo['ml_ncape'] = np.round(thermo['mlcape'] / ((thermo['ml_el_z'] - thermo['ml_lfc_z'])),1) 

        #--- DOWNDRAFT CAPE ---#
        # ---------------------------------------------------------------
        thermo['dcape'], thermo['dparcel_T'], thermo['dparcel_p'] = dcape(prof)                                     # calculate downdraft parcel properties

        try: 
            thermo['ecape'] = calc_ecape(z, p, T, general['spec_humidity'], u, v, 'most_unstable').m
        except:
            thermo['ecape'] = ma.masked
            warnings.warn("ECAPE could not be computed for this sounding (calculation error)", Warning)
            pass

        #--- PBL ---#
        # ---------------------------------------------------------------
        thermo['pbl_top'] = pbl_top(prof) 

        #--- DGZ ---#
        # ---------------------------------------------------------------
        thermo['dgz'] = dgz(prof)

        #--- HGZ ---#
        # ---------------------------------------------------------------
        thermo['hgz'] = hgz(prof)

        #--- LAPSE RATES ---#
        # ---------------------------------------------------------------
        thermo['lr_36km'] = lapse_rate(prof, 3000, 6000, pres=False)
        thermo['lr_03km'] = lapse_rate(prof, 0, 3000, pres=False) 
        thermo['lr_max']  = max_lapse_rate(prof, lower=0, upper=6000, 
                                         interval=250, depth=2000)
        
        #--- TEMPERATURE ADVECTION ---#
        # ---------------------------------------------------------------
        #returns temp_adv (C/hr) array and 2D array of top and bottom bounds of temp advection layer (mb)
        thermo['temp_adv'] = inferred_temp_adv(prof, lat=self.clean_data['site_info']['site-latlon'][0])
        ####################################################################
        
        



        ####################################################################
        ### KINEMATIC VALUES ###
        ####################################################################
        #--- LAPSE RATES ---#
        # ---------------------------------------------------------------   
        kinem['eil'] = effective_inflow_layer(prof, ecape=100, ecinh=- 250)
        kinem['eil_z'] = [to_agl(prof, hght(prof, kinem['eil'][0])), to_agl(prof, hght(prof, kinem['eil'][1]))]

        #--- STORM MOTION ---#
        # ---------------------------------------------------------------   
        sm_rm = bunkers_storm_motion(prof)[0:2] 
        sm_lm = bunkers_storm_motion(prof)[2:4] 
        sm_mw = mean_wind(prof, pbot=850, ptop=250)

        if ma.is_masked(sm_rm[0]) == True:
            try:
                kinem['sm_rm'], kinem['sm_lm'], kinem['sm_mw'] = mpcalc.bunkers_storm_motion(p, u, v, z)
                kinem['sm_rm'], kinem['sm_lm'], kinem['sm_mw'] = kinem['sm_rm'].m, kinem['sm_lm'].m, kinem['sm_mw'].m
            except:
                kinem['sm_rm'], kinem['sm_lm'], kinem['sm_mw'] = ma.masked, ma.masked, ma.masked
                warnings.warn("Bunkers Storm Motion could not be computed for this sounding (not enough data)", Warning)
                pass
        elif np.isnan(sm_rm[0]) == True:
            kinem['sm_rm'], kinem['sm_lm'], kinem['sm_mw'] = ma.masked, ma.masked, ma.masked
            warnings.warn("Bunkers Storm Motion could not be computed for this sounding (not enough data)", Warning)
        else:
            kinem['sm_rm'], kinem['sm_lm'], kinem['sm_mw'] = sm_rm, sm_lm, sm_mw
            
            
        #--- USER DEFINED SM PT ---#
        # ---------------------------------------------------------------  
        if ma.is_masked(kinem['sm_rm']) == False:
            if self.storm_motion in ['rm', 'RM', 'right', 'right_mover']:
                kinem['sm_u'] = kinem['sm_rm'][0]
                kinem['sm_v'] = kinem['sm_rm'][1]
            else:
                kinem['sm_u'] = kinem['sm_lm'][0]
                kinem['sm_v'] = kinem['sm_lm'][1]
        else:
            kinem['sm_u'] = ma.masked
            kinem['sm_v'] = ma.masked
            
                
        #--- DEVIANT TORNADO MOTION ---#
        # --------------------------------------------------------------- 
        if ma.is_masked(kinem['sm_rm']) == False:
            p300m = pres(prof, to_msl(prof, 300.))
            sfc = prof.pres[prof.sfc]
            mw_u_300, mw_v_300 = mean_wind(prof, pbot=sfc, ptop=p300m)
            kinem['dtm'] = ((kinem['sm_u']+mw_u_300)/2, (kinem['sm_u']+mw_v_300)/2)
        else:
            kinem['dtm'] = ma.masked
          
        
        #--- CORFIDI MSC MOTION ---#
        #----------------------------------------------------------------
        kinem['mcs'] = corfidi_mcs_motion(prof)


        #--- BULK SHEAR ---#
        # ---------------------------------------------------------------    
        sfc = prof.pres[prof.sfc]
        p500m = pres(prof, to_msl(prof, 500.))
        p3km = pres(prof, to_msl(prof, 3000.))
        p6km = pres(prof, to_msl(prof, 6000.))
        p1km = pres(prof, to_msl(prof, 1000.))

        shear_0_to_500  = wind_shear(prof, pbot=sfc, ptop=p500m)
        shear_0_to_1000 = wind_shear(prof, pbot=sfc, ptop=p1km)
        shear_1_to_3000 = wind_shear(prof, pbot=p1km, ptop=p3km)
        shear_3_to_6000 = wind_shear(prof, pbot=p3km, ptop=p6km)

        kinem['shear_0_to_500']  = comp2vec(shear_0_to_500[0], shear_0_to_500[1])[1]
        kinem['shear_0_to_1000'] = comp2vec(shear_0_to_1000[0], shear_0_to_1000[1])[1]
        kinem['shear_1_to_3000'] = comp2vec(shear_1_to_3000[0], shear_1_to_3000[1])[1]
        kinem['shear_3_to_6000'] = comp2vec(shear_3_to_6000[0], shear_3_to_6000[1])[1]
            
        #--- SRH ---#
        # ---------------------------------------------------------------
        if ma.is_masked(kinem['sm_rm']) == False:
            kinem['srh_0_to_500']  = helicity(prof, 0, 500., stu = kinem['sm_u'], stv = kinem['sm_v'])[0]
            kinem['srh_0_to_1000'] = helicity(prof, 0, 1000., stu = kinem['sm_u'], stv = kinem['sm_v'])[0]
            kinem['srh_1_to_3000'] = helicity(prof, 1000, 3000., stu = kinem['sm_u'], stv = kinem['sm_v'])[0]
            kinem['srh_3_to_6000'] = helicity(prof, 3000, 6000., stu = kinem['sm_u'], stv = kinem['sm_v'])[0]
        else:
            kinem['srh_0_to_500']  = ma.masked
            kinem['srh_0_to_1000'] = ma.masked
            kinem['srh_1_to_3000'] = ma.masked
            kinem['srh_3_to_6000'] = ma.masked
            warnings.warn("Storm Relative Helicity could not be computed for this sounding (no valid storm motion)", Warning)


        #--- SRW LAYERS ---#
        # --------------------------------------------------------------- 
        if ma.is_masked(kinem['sm_rm']) == False:
            def calc_srw_layer(prof, level):
                u, v = components(prof, p=pres(prof, to_msl(prof, level)))
                sru = u - kinem['sm_u']
                srv = v - kinem['sm_v']
                return mpcalc.wind_speed(sru*units.kts, srv*units.kts)
            try:
                kinem['srw_0_to_500']  = (calc_srw_layer(prof, 500)+ calc_srw_layer(prof, 0))/2
                kinem['srw_0_to_1000'] = (calc_srw_layer(prof, 1000) + calc_srw_layer(prof, 0))/2
                kinem['srw_1_to_3000'] = (calc_srw_layer(prof, 3000) + calc_srw_layer(prof, 1000))/2
                kinem['srw_3_to_6000'] = (calc_srw_layer(prof, 6000) + calc_srw_layer(prof, 3000))/2
            except:
                kinem['srw_0_to_500']  = ma.masked
                kinem['srw_0_to_1000'] = ma.masked
                kinem['srw_1_to_3000'] = ma.masked
                kinem['srw_3_to_6000'] = ma.masked
                pass
        else:
            kinem['srw_0_to_500']  = ma.masked
            kinem['srw_0_to_1000'] = ma.masked
            kinem['srw_1_to_3000'] = ma.masked
            kinem['srw_3_to_6000'] = ma.masked
            warnings.warn("Storm Relative Wind could not be computed for this sounding (no valid storm motion)", Warning)
            
        #--- SRV ---#
        # ---------------------------------------------------------------
        # adopted from Sam Brandt (2022)    
        if ma.is_masked(kinem['sm_rm']) == False: 
            # CONVERT TO m/s (uses `sm_u, sm_v` calculated above)
            u_ms = (intrp['uINTRP']/1.94384)
            v_ms = (intrp['vINTRP']/1.94384)
            sm_u_ms = ((intrp['uINTRP'] - kinem['sm_u'])/1.94384)
            sm_v_ms = ((intrp['vINTRP'] - kinem['sm_v'])/1.94384)

            # INTEROPLATED SRW (send back to knots)
            srw = mpcalc.wind_speed(sm_u_ms*units('m/s'), sm_v_ms*units('m/s'))
            kinem['srw'] = (srw.m*1.94384)

            # SHEAR COMPONENTS FOR VORT CALC
            # calc example = change in u over change in z
            dudz = (u_ms[2::]-u_ms[0:-2]) / (intrp['zINTRP'][2::]-intrp['zINTRP'][0:-2])
            dvdz = (v_ms[2::]-v_ms[0:-2]) / (intrp['zINTRP'][2::]-intrp['zINTRP'][0:-2])
            dudz = np.insert(dudz,0,dudz[0])
            dudz = np.insert(dudz,-1,dudz[-1])
            dvdz = np.insert(dvdz,0,dvdz[0])
            dvdz = np.insert(dvdz,-1,dvdz[-1])
            # Shear magnitude, 
            shear=(np.sqrt(dudz**2+dvdz**2)+0.0000001)
            # Vorticity components
            uvort=-dvdz
            vvort=dudz
            # Total horizontal vorticity
            kinem['vort'] = np.sqrt(uvort**2 + vvort**2)
            # Total streamwise vorticity
            kinem['swv'] = abs((sm_u_ms*uvort+sm_v_ms*vvort)/(np.sqrt(sm_u_ms**2+sm_v_ms**2)))
            # Streamwiseness fraction
            kinem['swv_perc'] = (kinem['swv']/shear)*100

            # layer average streamwiseness and total streamwise vorticity
            kinem['swv_perc_0_to_500']  = np.mean(kinem['swv_perc'][0:5])
            kinem['swv_perc_0_to_1000'] = np.mean(kinem['swv_perc'][0:10])
            kinem['swv_perc_1_to_3000'] = np.mean(kinem['swv_perc'][10:30])
            kinem['swv_perc_3_to_6000'] = np.mean(kinem['swv_perc'][30:60])
            kinem['swv_0_to_500']       = np.mean(kinem['swv'][0:5])
            kinem['swv_0_to_1000']      = np.mean(kinem['swv'][0:10])
            kinem['swv_1_to_3000']      = np.mean(kinem['swv'][10:30])
            kinem['swv_3_to_6000']      = np.mean(kinem['swv'][30:60])
        else:
            kinem['srw']                = ma.masked
            kinem['swv']                = ma.masked
            kinem['swv_perc']           = ma.masked
            kinem['vort']               = ma.masked
            kinem['swv_perc_0_to_500']  = ma.masked
            kinem['swv_perc_0_to_1000'] = ma.masked
            kinem['swv_perc_1_to_3000'] = ma.masked
            kinem['swv_perc_3_to_6000'] = ma.masked
            kinem['swv_0_to_500']       = ma.masked
            kinem['swv_0_to_1000']      = ma.masked
            kinem['swv_1_to_3000']      = ma.masked
            kinem['swv_3_to_6000']      = ma.masked
            warnings.warn("Streamwise Vorticity could not be computed for this sounding (no valid storm motion)", Warning)
        
        # MEAN RELATIVE HUMIDITY CALCULATIONS ----------------------------------------------------------
        general['rh_0_500']  = np.mean(intrp['rhINTRP'][0:5])
        general['rh_0_1000'] = np.mean(intrp['rhINTRP'][0:10])
        general['rh_1_3000'] = np.mean(intrp['rhINTRP'][10:30])
        general['rh_3_6000'] = np.mean(intrp['rhINTRP'][30:60])
        general['rh_6_9000'] = np.mean(intrp['rhINTRP'][60:90])
        

        general['w_0_500']  = np.mean(intrp['mrINTRP'][0:5]) 
        general['w_0_1000'] = np.mean(intrp['mrINTRP'][0:10]) 
        general['w_1_3000'] = np.mean(intrp['mrINTRP'][10:30]) 
        general['w_3_6000'] = np.mean(intrp['mrINTRP'][30:60]) 
        general['w_6_9000'] = np.mean(intrp['mrINTRP'][60:90]) 
        
        return general, thermo, kinem, intrp 

    
    
    ######################################################################################################
    ### PRINT FUNCTION -- PRINT A FEW VALUES ###
    ######################################################################################################  
    def print_vals(self):
        thermo = self.calc()[1]
        kinem  = self.calc()[2]
        print(' ')
        print(f'> THERMODYNAMICS --------------------------------------------- ')
        print(f"--- SBCAPE: {np.round(thermo['sbcape'], 1)} | MUCAPE: {np.round(thermo['mucape'], 1)} | MLCAPE: {np.round(thermo['mlcape'], 1)} | ECAPE: {np.round(thermo['ecape'], 1)}")
        print(f"--- MU 0-3: {np.round(thermo['mu3cape'], 1)} | MU 0-6: {np.round(thermo['mu6cape'], 1)} | SB 0-3: {np.round(thermo['sb3cape'], 1)} | SB 0-6: {np.round(thermo['sb6cape'], 1)}")
        print(' ')
        print(f'> KINEMATICS ------------------------------------------------- ')
        print(f"--- 0-500 SRW: {np.round(kinem['srw_0_to_500'], 1)} | 0-500 SWV: {np.round(kinem['swv_0_to_500'],3)} | 0-500 SHEAR: {np.round(kinem['shear_0_to_500'], 1)} | 0-500 SRH: {np.round(kinem['srh_0_to_500'], 1)}")
        print(f"--- 1-3km SRW: {np.round(kinem['srw_1_to_3000'], 1)} | 1-3km SWV: {np.round(kinem['swv_1_to_3000'],3)} | 1-3km SHEAR: {np.round(kinem['shear_1_to_3000'], 1)} | | 1-3km SRH: {np.round(kinem['srh_1_to_3000'], 1)}")
        print(f'============================================================== ')
        print(" ")



