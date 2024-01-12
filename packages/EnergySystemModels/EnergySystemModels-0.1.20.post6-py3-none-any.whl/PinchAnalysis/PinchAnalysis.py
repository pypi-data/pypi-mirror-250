import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Object:
    def __init__(self, df):
        #initialisation 


        # Créer la colonne 'integration' et la remplir avec True si elle n'existe pas
        if 'integration' not in df.columns:
            df['integration'] = True
        # Remplacer les valeurs NaN par True
        df['integration'].fillna(True, inplace=True)

        # Sélectionner les flux à intégrer
        self.stream_list = df[df['integration'] == True].copy()  # Utilisez .copy() pour éviter le Warning

        self.rowCount = len(self.stream_list)

        # Créer la colonne 'StreamType'
        self.stream_list['StreamType'] = np.where(self.stream_list['Ti'] > self.stream_list['To'], 'HS', 'CS')

        # Créer de nouvelles colonnes pour les températures décalées
        self.stream_list['STi'] = np.where(self.stream_list['StreamType'] == 'HS',
                                                  self.stream_list['Ti'] - self.stream_list['dTmin2'],
                                                  self.stream_list['Ti'] + self.stream_list['dTmin2'])

        self.stream_list['STo'] = np.where(self.stream_list['StreamType'] == 'HS',
                                                  self.stream_list['To'] - self.stream_list['dTmin2'],
                                                  self.stream_list['To'] + self.stream_list['dTmin2'])

         # Calculer T_shifted directement dans la classe
        T_shifted = np.concatenate([self.stream_list['STi'].values, self.stream_list['STo'].values])
        T_shifted = np.sort(np.unique(T_shifted))[::-1]
        self.df_T_shifted = pd.DataFrame({'T_shifted': T_shifted})



                # Créer le DataFrame df_intervals
        self.df_intervals = pd.DataFrame({'Tsup': T_shifted[:-1], 'Tinf': T_shifted[1:]})
        self.df_intervals['IntervalName'] = self.df_intervals['Tsup'].astype(str) + '-' + self.df_intervals['Tinf'].astype(str)

        self.decomposition_flux()
        self.surplus_deficit()
        self.composite_curve()
        self.below_above_stream()
        self.find_heat_exchange_combinations()


    def decomposition_flux(self):
        # Ajouter des colonnes pour le nom du flux et la valeur de mCp à df_intervals
        self.df_intervals['StreamName'] = [[] for _ in range(len(self.df_intervals))]
        self.df_intervals['mCp'] = [[] for _ in range(len(self.df_intervals))]
        self.df_intervals['StreamType'] = [[] for _ in range(len(self.df_intervals))]  # Add this line


        # Parcourir chaque intervalle
        for idx, row in self.df_intervals.iterrows():

            # Parcourir chaque flux
            for i in range(self.rowCount):
                # Tester la condition spécifique (StreamType[i] == "CS")
                if (self.stream_list['StreamType'].iloc[i] == "CS") and (self.stream_list['STi'].iloc[i] < row['Tsup']) and (self.stream_list['STo'].iloc[i] > row['Tinf']):

                    # Flux dans l'intervalle
                    #self.df_intervals.at[idx, 'mCp'].append(-self.stream_list['mCp'][i])
                    #self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'][i])
                    #self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'][i])  # Add this line
                    self.df_intervals.at[idx, 'mCp'].append(-self.stream_list['mCp'].iloc[i])
                    self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'].iloc[i])
                    self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'].iloc[i])





                # Tester la condition spécifique (StreamType[i] == "HS")
                #elif (self.stream_list['StreamType'][i] == "HS") and (self.stream_list['STi'][i] > row['Tinf']) and (self.stream_list['STo'][i] < row['Tsup']):
                elif (self.stream_list['StreamType'].iloc[i] == "HS") and (self.stream_list['STi'].iloc[i] > row['Tinf']) and (self.stream_list['STo'].iloc[i] < row['Tsup']):
 

                    # Flux dans l'intervalle
                    #self.df_intervals.at[idx, 'mCp'].append(self.stream_list['mCp'][i])
                    self.df_intervals.at[idx, 'mCp'].append(self.stream_list['mCp'].iloc[i])
                    #self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'][i])
                    self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'].iloc[i])
                    #self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'][i]) 
                    self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'].iloc[i]) 



        # Utiliser explode pour dupliquer les lignes pour chaque valeur de mCp
        self.df_intervals = self.df_intervals.explode(['StreamName', 'mCp', 'StreamType']).reset_index(drop=True)
        self.df_intervals = self.df_intervals.sort_values(by=['StreamName', 'Tsup']).reset_index(drop=True)
        self.df_intervals["delta_T"]=self.df_intervals['Tsup']-self.df_intervals['Tinf']
        self.df_intervals["delta_H"]=self.df_intervals["delta_T"]*self.df_intervals["mCp"]



    def plot_streams_and_temperature_intervals(self,figsize=(8, 6)):

      # Extract necessary columns from the DataFrame
      StreamType = self.stream_list['StreamType']
      names = self.stream_list['name']
      STi = self.stream_list['STi']
      STo = self.stream_list['STo']
      mCp=self.stream_list['mCp']

      # Create a new figure
      plt.figure(figsize=figsize)

      # Plot the streams with shifted temperature scale and color based on StreamType
      for i in range(len(names)):
        #if StreamType[i] == 'HS':
        #  plt.plot([names[i], names[i]], [STi[i], STo[i]], color='red', label=f'Stream {names[i]}')

        if StreamType.iloc[i] == 'HS':
            plt.plot([names.iloc[i], names.iloc[i]], [STi.iloc[i], STo.iloc[i]], color='red', label=f'Stream {names.iloc[i]}')

          # Ajouter une flèche à la fin du segment
            # plt.annotate('', xy=(names[i], STo[i]), xytext=(names[i], STo[i] + 1),
            #           arrowprops=dict(arrowstyle='->', color='red', lw=1), annotation_clip=False)
            plt.annotate('', xy=(names.iloc[i], STo.iloc[i]), xytext=(names.iloc[i], STo.iloc[i] + 1),
                arrowprops=dict(arrowstyle='->', color='red', lw=1), annotation_clip=False)

        else:
          plt.plot([names[i], names[i]], [STi[i], STo[i]], color='blue', label=f'Stream {names[i]}')

          plt.annotate('', xy=(names[i], STo[i]), xytext=(names[i], STo[i] - 1),
                      arrowprops=dict(arrowstyle='->', color='blue', lw=1), annotation_clip=False)


      # Set y-axis ticks and labels
      y_ticks = sorted(set(STi) | set(STo))
      plt.yticks(y_ticks)

      # Add horizontal dashed lines for each temperature value
      for temp in y_ticks:
          plt.axhline(y=temp, linestyle='--', color='gray', alpha=0.7)

      # Set axis labels and title
      plt.xlabel('Stream name')
      plt.ylabel('Shifted temperature (°C)')
      plt.title('Streams and temperature intervals')

      # Set x-axis tick labels with mCp values
      plt.xticks(range(len(names)), [f'{name}\n($mCp={{{mCp_val:.2f}}}$)' for name, mCp_val in zip(names, mCp)],
               fontsize=8)
      
       # Show the Pinch Temperature label on the y-axis
      plt.text(0, self.Pinch_Temperature, f'Pinch_Temperature = {self.Pinch_Temperature} °C',
             verticalalignment='bottom', horizontalalignment='left')
    
      # Show grid
      plt.grid(True)

      # Show the plot without legend
      plt.show()

    def surplus_deficit(self):
      # Group by 'IntervalName' and aggregate the values
      self.df_surplus_deficit = self.df_intervals.groupby('IntervalName').agg({
          'Tsup': 'first',  # Keep the first value
          'Tinf': 'first',  # Keep the first value
          'StreamName':  lambda x: list(x),  # Keep the first value
          'mCp': 'sum',  # Sum the 'mCp' values
          'StreamType': lambda x: list(x),  # Keep the first value
          'delta_T': 'first',  # Sum the 'delta_T' values
          'delta_H': 'sum'  # Sum the 'delta_H' values
      }).reset_index()

      # Sort by 'Tsup' in descending order
      self.df_surplus_deficit = self.df_surplus_deficit.sort_values(by='Tsup', ascending=False)

      self.df_surplus_deficit['cumulative_delta_H'] =self.df_surplus_deficit['delta_H'].cumsum()

      self.Heating_duty=abs(min(self.df_surplus_deficit['cumulative_delta_H']))
      if min(self.df_surplus_deficit['cumulative_delta_H']) >= 0:
        self.Heating_duty = 0
      else:
         self.Heating_duty = abs(min(self.df_surplus_deficit['cumulative_delta_H']))



      # Créer une ligne avec la valeur 0 pour 'cumulative_delta_H'
      self.cumulative_delta_H = pd.concat([pd.Series([0], name='cumulative_delta_H'), self.df_surplus_deficit['cumulative_delta_H']], ignore_index=True)

      # Ajouter la nouvelle ligne à self.Heating_duty
      self.cumulative_delta_H = pd.DataFrame(self.Heating_duty + self.cumulative_delta_H)

      # Concaténer les deux colonnes dans un nouveau DataFrame
      self.GCC = pd.concat([self.df_T_shifted, self.cumulative_delta_H], axis=1)

      # Récupérer la valeur de cumulative_delta_H correspondante
      self.Cooling_duty = self.GCC.loc[self.GCC['T_shifted'].idxmin(), 'cumulative_delta_H']

      # Récupérer la valeur de T_shifted correspondante à cumulative_delta_H nulle
      self.Pinch_Temperature = self.GCC.loc[self.GCC[self.GCC['cumulative_delta_H'] == 0].index, 'T_shifted'].values[0]
      


    def plot_GCC(self):

      # Tracer la courbe de composition avec les axes inversés
      plt.plot(self.GCC['cumulative_delta_H'], self.GCC['T_shifted'], marker='o', label='Courbe de Composition')

      # Ajouter des étiquettes et un titre au graphe
      plt.xlabel('Net heat flow (kW)')
      plt.ylabel('Shifted temperature (°C)')
      plt.title('Grand composite curve')

      # Ajouter la grille
      plt.grid(True)

      # Trouver l'index du maximum de T_shifted
      max_index = self.GCC['T_shifted'].idxmax()

      # Afficher la valeur de Heating_duty au niveau du maximum de T_shifted
      plt.text(self.GCC['cumulative_delta_H'][max_index], self.GCC['T_shifted'][max_index], f'Heating_duty = {self.Heating_duty} kW', verticalalignment='bottom', horizontalalignment='left')

      # Trouver l'index du minimum de T_shifted
      min_index = self.GCC['T_shifted'].idxmin()

      # Afficher la valeur de Cooling_duty au niveau du minimum de T_shifted
      plt.text(self.GCC['cumulative_delta_H'][min_index], self.GCC['T_shifted'][min_index], f'Cooling_duty = {self.Cooling_duty} kW', verticalalignment='bottom', horizontalalignment='right')


      # Afficher la valeur de Pinch_Temperature sur l'axe des ordonnées
      plt.text(0, self.Pinch_Temperature, f'Pinch_Temperature = {self.Pinch_Temperature} °C', verticalalignment='bottom', horizontalalignment='left')


      # Afficher le graphe
      plt.show()

    def composite_curve(self):
      # Définition des fonctions d'agrégation pour chaque colonne
      agg_functions = {'delta_H': 'sum', 'mCp': 'sum', 'Tsup': 'last', 'Tinf': 'last', 'StreamName': lambda x: list(x)}

      # Groupement par IntervalName et StreamType avec application des fonctions d'agrégation
      composite_curve = self.df_intervals.groupby(['IntervalName', 'StreamType']).agg(agg_functions).reset_index()
      composite_curve = composite_curve.sort_values(by=['StreamType', 'Tsup'], ascending=[True, True])

      # Créer des copies des DataFrames résultants
      self.cold_composite_curve = composite_curve[composite_curve['StreamType'] == 'CS'].copy()
      self.hot_composite_curve = composite_curve[composite_curve['StreamType'] == 'HS'].copy()

      # Calcul de la somme cumulée par StreamType
      self.cold_composite_curve['delta_H'] =-1*self.cold_composite_curve['delta_H']
      self.cold_composite_curve['mCp'] =-1*self.cold_composite_curve['mCp']
      self.cold_composite_curve['cumulative_delta_H'] = self.cold_composite_curve['delta_H'].cumsum()
      self.hot_composite_curve['cumulative_delta_H'] = self.hot_composite_curve['delta_H'].cumsum()

      self.cold_stream=max(self.cold_composite_curve['cumulative_delta_H'])
      self.hot_stream=max(self.hot_composite_curve['cumulative_delta_H'])

      self.heat_recovery=self.hot_stream-self.Cooling_duty
      #self.heat_recovery=self.cold_stream-self.Heating_duty


      # Afficher le résultat
      self.cold_composite_curve
      self.hot_composite_curve


      # Création du nouveau dataframe avec une ligne supplémentaire
      hcc_data = {'T': [self.hot_composite_curve['Tinf'].min()] + self.hot_composite_curve['Tsup'].tolist(),
                  'Q': [0] + self.hot_composite_curve['cumulative_delta_H'].tolist()}



      self.df_hcc = pd.DataFrame(hcc_data)
      self.df_hcc


      # Création du nouveau dataframe avec une ligne supplémentaire
      ccc_data = {'T': [self.cold_composite_curve['Tinf'].min()] + self.cold_composite_curve['Tsup'].tolist(),
                  'Q': [0] + self.cold_composite_curve['cumulative_delta_H'].tolist()+self.Cooling_duty}

      self.df_ccc = pd.DataFrame(ccc_data)
      self.df_ccc


    def plot_composites_curves(self):
            # Assurer que les deux dataframes ont la même longueur
      length = max(len(self.df_hcc), len(self.df_ccc))
      self.df_hcc = self.df_hcc.reindex(range(length)).fillna(method='ffill')
      self.df_ccc = self.df_ccc.reindex(range(length)).fillna(method='ffill')

      # Tracer les données originales
      plt.plot(self.df_hcc['Q'], self.df_hcc['T'], label='courbe composite du flux chaud', marker='o')
      plt.plot(self.df_ccc['Q'], self.df_ccc['T'], label='courbe composite du flux froid', marker='o')

      # Déterminer les limites pour la région à remplir
      q_min_fill = max(self.df_hcc['Q'].min(), self.df_ccc['Q'].min())
      q_max_fill = min(self.df_hcc['Q'].max(), self.df_ccc['Q'].max())

      # Créer une séquence linéaire pour Q dans la zone à remplir
      q_fill = np.linspace(q_min_fill, q_max_fill, 100)

      # Créer des masques pour exclure certaines parties de la zone remplie
      mask_before_ccc = q_fill < self.df_hcc['Q'].min()
      mask_after_ccf = q_fill > self.df_ccc['Q'].max()

      # Appliquer les masques pour exclure les parties indésirables
      q_fill_masked = q_fill[~(mask_before_ccc | mask_after_ccf)]
      t_ccc_fill = np.interp(q_fill_masked, self.df_hcc['Q'], self.df_hcc['T'])
      t_ccf_fill = np.interp(q_fill_masked, self.df_ccc['Q'], self.df_ccc['T'])

      # Tracer la zone remplie avec rotation
      plt.fill_between(q_fill_masked, t_ccc_fill, t_ccf_fill, color='green', alpha=0.3)


      # Ajouter des lignes pointillées
      for index, row in self.df_hcc.iterrows():
          plt.axvline(x=row['Q'], color='gray', linestyle='--')
          plt.axhline(y=row['T'], color='gray', linestyle='--')

      for index, row in self.df_ccc.iterrows():
          plt.axvline(x=row['Q'], color='gray', linestyle='--')
          plt.axhline(y=row['T'], color='gray', linestyle='--')

      # Ajouter des étiquettes et un titre
      plt.xlabel('Heat flow (kW)')
      plt.ylabel('Shifted temperature (°C)')
      plt.title('Shifted hot and cold composite curves')
      plt.legend()  # Ajouter la légende

      # Afficher le graphique
      plt.show()


    def below_above_stream(self):
        new_rows = []

        # Division de chaque ligne en deux
        for index, row in self.stream_list.iterrows():
            row_below = row.copy()
            row_below['STo'] = self.Pinch_Temperature
            new_rows.append(row_below)

            row_above = row.copy()
            row_above['STi'] = self.Pinch_Temperature
            new_rows.append(row_above)

        # Création du nouveau DataFrame
        df_divided = pd.DataFrame(new_rows).sort_values(by=['id', 'STi']).reset_index(drop=True)

        for i, row in df_divided.iterrows():
            if row['StreamType'] == "CS":
                df_divided.at[i, 'Ti'] = row['STi'] + row['dTmin2']
                df_divided.at[i, 'To'] = row['STo'] + row['dTmin2']
            else:  # Pour les flux "HS"
                df_divided.at[i, 'Ti'] = row['STi'] - row['dTmin2']
                df_divided.at[i, 'To'] = row['STo'] - row['dTmin2']

        # DataFrame df_above (STi et STo >= pinch_temperature)
        self.stream_list_above = df_divided[(df_divided['STi'] >= self.Pinch_Temperature) & (df_divided['STo'] >= self.Pinch_Temperature) & (df_divided['STi'] != df_divided['STo'])]

        # DataFrame df_below (STi et STo <= pinch_temperature)
        self.stream_list_below = df_divided[(df_divided['STi'] <= self.Pinch_Temperature) & (df_divided['STo'] <= self.Pinch_Temperature) & (df_divided['STi'] != df_divided['STo'])]



    def find_heat_exchange_combinations(self):
       
        # Extract hot and cold streams above pinch
        hot_streams_above = self.stream_list_above[self.stream_list_above['StreamType'] == 'HS']
        cold_streams_above = self.stream_list_above[self.stream_list_above['StreamType'] == 'CS']

        # Find all combinations where mCpH <= mCpC for above pinch
        self.combinations_above = [(hot_stream['name'], cold_stream['name'])
                              for _, hot_stream in hot_streams_above.iterrows()
                              for _, cold_stream in cold_streams_above.iterrows()
                              if hot_stream['mCp'] <= cold_stream['mCp']]

        # Extract hot and cold streams below pinch
        hot_streams_below = self.stream_list_below[self.stream_list_below['StreamType'] == 'HS']
        cold_streams_below = self.stream_list_below[self.stream_list_below['StreamType'] == 'CS']

        # Find all combinations where mCpHS >= mCpCS for below pinch
        self.combinations_below = [(hot_stream['name'], cold_stream['name'])
                              for _, hot_stream in hot_streams_below.iterrows()
                              for _, cold_stream in cold_streams_below.iterrows()
                              if hot_stream['mCp'] >= cold_stream['mCp']]

    

    # Use the function with the given datasets
   