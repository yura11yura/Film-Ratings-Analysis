import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

all_sites = pd.read_csv(r"C:\Users\Yura\PycharmProjects\MovieRatings\.venv\all_sites_scores.csv")
fandango = pd.read_csv(r"C:\Users\Yura\PycharmProjects\MovieRatings\.venv\fandango_scrape.csv")
output = open("output.txt", 'w')
separation = '-'*60

# Fandango scatterplot
# Y axis - Votes, X axis - Rating
plt.figure(figsize=[9,4], dpi=150)
sns.scatterplot(data = fandango, y = 'VOTES', x = 'RATING')

plt.savefig(r"plots\fandango_votes_rating.jpg")

# Correlation of the DataFrame
output.write("1) Fandango DataFrame correlation\n" +
             fandango.corr(numeric_only=True).to_string() + f"\n{separation}\n")

# Get year from date-time row 'FILM'
fandango['YEAR'] = fandango['FILM'].apply(lambda str: str[-5:-1])
output.write("2) Get year from date-time row 'FILM'\n" +
             fandango['YEAR'].head(10).to_string() + f"\n{separation}\n")

# Fandango film count grouped by release year
output.write("3) Fandango film count grouped by release year\n" +
             fandango.groupby('YEAR', as_index=True, sort=False).size().to_string() + f"\n{separation}\n")

# Fandango histplot
# Y axis - Count, X axis - Year
plt.figure(figsize=[10, 4])
tmp = fandango.groupby('YEAR', as_index=True, sort=False).size()
g = sns.histplot(data=fandango, x='YEAR', shrink=0.7, hue = 'YEAR', linewidth=0, alpha=1)
g.legend_.remove()

plt.savefig(r"plots\fandango_count_year.jpg")

# Fandango films sorted by umber of votes
output.write("4) Fandango films sorted by umber of votes\n" +
             fandango.sort_values('VOTES', ascending=False).head(10).to_string() + f"\n{separation}\n")

# Number of films without votes
output.write("5) Fandango number of films without votes\n" +
             str(fandango[fandango['VOTES'] == 0].count()['FILM']) + f"\n{separation}\n")

# Fandango films which have more than 0 votes
fandango_w_votes = fandango[fandango['VOTES'] > 0]
output.write("6) Fandango films with more than 0 votes\n" +
             fandango_w_votes.head(10).to_string() + f"\n{separation}\n")

# Fandango kdeplot
# Y axis - Density, X axis - True Rating & Stars Displayed
plt.figure(figsize=[12,5])
sns.kdeplot(data=fandango, x='RATING', clip =[0.7,5], bw_adjust=0.6, fill=True)
sns.kdeplot(data=fandango, x='STARS', clip =[0.7,5], bw_adjust=0.5, fill=True)
plt.legend(['True Rating', 'Stars Displayed'], loc=(1.1,0.8))

plt.savefig(r"plots\fandango_kde_plot.jpg")

# Fandango difference between stars and rating
fandango['STARS_DIFF'] = round(abs(fandango['STARS']-fandango['RATING']), 1)
output.write("7) Fandango difference between stars and rating\n" +
             fandango.head(10).to_string() + f"\n{separation}\n")

# Fandango countplot
# Y axis - Count, X axis - Stars difference
plt.figure(figsize=(12,4),dpi=150)
sns.countplot(data=fandango, x='STARS_DIFF')

plt.savefig(r"plots\fandango_stars_diff")

# Fandango film with 1 star difference
output.write("8) Fandango film with 1 star difference between user ratings and stars displayed\n" +
             fandango[fandango['STARS_DIFF'] == 1].to_string() + f"\n{separation}\n")

# RottenTomatoes scatterplot
# Y axis - User rating, X axis - RT rating
plt.figure(figsize=[11,5], dpi=140)
plt.xlim(0, 100)
sns.scatterplot(data=all_sites, x='RottenTomatoes', y='RottenTomatoes_User')

plt.savefig(r"plots\rottentomatoes_user_rt")

# RottenTomatoes difference between user ratings and RT rating
all_sites['Rotten_diff'] = all_sites['RottenTomatoes']-all_sites['RottenTomatoes_User']
output.write("9) RottenTomatoes difference between user ratings and RT rating\n" +
             all_sites.head(10).to_string() + f"\n{separation}\n")

# Rotten tomatoes mean difference
output.write("10) RottenTomatoes mean difference\n" +
             str(round(all_sites['Rotten_diff'].apply(lambda num: abs(num)).mean(), 4)) + f"\n{separation}\n")

# RottenTomatoes histplot
# Y axis - Count, X axis - difference
plt.figure(figsize=[10,5], dpi=180)
plt.title("RT Critics Score minus RT User Score")
sns.histplot(data=all_sites, x='Rotten_diff', bins=25, kde=True)

plt.savefig(r"plots\rottentomatoes_rt_minus_user.jpg")

# RottenTomatoes histplot
# Y axis - Count, X axis - abs(difference)
plt.figure(figsize=[11,5], dpi=140)
temp = all_sites['Rotten_diff'].apply(lambda num: abs(num))
sns.histplot(data=temp, bins=25, kde=True)
plt.title('Abs Difference between RT Critics Score and RT User Score')

plt.savefig(r"plots\rottentomatoes_user_rt_abs.jpg")

# RottenTomatoes 5 films ranked highest by users compared to critics
output.write("11) RottenTomatoes 5 films ranked highest by users compared to critics\n" +
             all_sites.sort_values('Rotten_diff').head(5)[['FILM', 'Rotten_diff']].to_string() + f"\n{separation}\n")

# RottenTomatoes 5 films ranked highest by critics compared to users
output.write("12) RottenTomatoes 5 films ranked highest by critics compared to users\n" +
             all_sites.sort_values('Rotten_diff', ascending=False).head(5)[['FILM', 'Rotten_diff']].to_string() + f"\n{separation}\n")

# MetaCritic scatterplot
# Y axis - User rating, X axis - MC rating
plt.figure(figsize=[12,5], dpi=130)
sns.scatterplot(data=all_sites, x='Metacritic', y='Metacritic_User')

plt.savefig(r"plots\metacritic_user_mc.jpg")

# IMDB scatterplot
# Y axis - MC User vote count, X axis - IMDB user vote count
plt.figure(figsize=[11,5], dpi=140)
sns.scatterplot(data=all_sites, x='Metacritic_user_vote_count', y='IMDB_user_vote_count')

plt.savefig(r"plots\imdb_metacritic_user_count.jpg")

# IMDB film with highest number of votes
output.write("13) IMDB film with highest number of votes\n" +
             all_sites.iloc[all_sites['IMDB_user_vote_count'].idxmax()].to_string() + f"\n{separation}\n")

# MetaCritic film with highest number of votes
output.write("14) MetaCritic film with highest number of votes\n" +
             all_sites.nlargest(1, 'Metacritic_user_vote_count').to_string() + f"\n{separation}\n")

# Merging fandango dataframe with all_sites
fandango_w_all_sites = pd.merge(left=fandango, right=all_sites, how='inner', on='FILM')
output.write("15) Fandango with all_sites\n" +
             fandango_w_all_sites.head(10).to_string() + f"\n{separation}\n")


# Normalize ratings to range 0-5
fandango_w_all_sites[['RT_Norm', 'RTU_Norm']] = round(fandango_w_all_sites[['RottenTomatoes', 'RottenTomatoes_User']]/100*5, 1)
fandango_w_all_sites['Meta_Norm'] = round(fandango_w_all_sites['Metacritic']/100*5, 1)
fandango_w_all_sites['Meta_U_Norm'] = round(fandango_w_all_sites['Metacritic_User']/10*5, 1)
fandango_w_all_sites['IMDB_Norm'] = round(fandango_w_all_sites['IMDB']/10*5, 1)
output.write("16) Normalize all ratings to range 0-5\n" +
             fandango_w_all_sites[['STARS','RATING','RT_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']].head(10).to_string() + f"\n{separation}\n")

# New DataFrame containing only normalized ratings
norm_scores = pd.DataFrame()
norm_scores = fandango_w_all_sites[['STARS', 'RATING', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm']]

# KDE plot comparing normalized scores of all websites
# Y axis - Density, X axis - Ratings
def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legend_handles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)

fig, ax = plt.subplots(figsize=[12,5], dpi=150)
sns.kdeplot(data=norm_scores, fill=True, clip=[0,5], ax=ax)
move_legend(ax, "upper left")

plt.savefig(r"plots\normalized_comparison_kde.jpg")

# KDE plot comparing fandango
# Y axis - Density, X axis - Ratings
fig, ax = plt.subplots(figsize=[11,5], dpi=150)
tmp = fandango_w_all_sites[['RT_Norm', 'STARS']]
sns.kdeplot(data=tmp, ax=ax, fill=True, clip=[0,5])
move_legend(ax, 'upper left')

plt.savefig(r"plots\fandango_rt_norm_kde.jpg")

# Histplot comparing all ratings from all websites
plt.subplots(figsize=(10,5), dpi=150)
sns.histplot(fandango_w_all_sites, bins=50)

plt.savefig(r"plots\comparison_hist.jpg")

# Comparison clustermap
# Y axis - Films, X axis - Ratings
plt.figure(figsize=(10, 10), dpi = 150)
my_clustermap = sns.clustermap(norm_scores, col_cluster=False)
tmp = fandango_w_all_sites['FILM']
int_labels = []
text_labels = []
for tick in my_clustermap.ax_heatmap.get_yticklabels():
    int_labels.append(int(tick.get_text()))
    text_labels.append(tmp.iloc[int(tick.get_text())])
my_clustermap.ax_heatmap.set_yticks(my_clustermap.ax_heatmap.get_yticks(), labels=text_labels);

plt.savefig(r"plots\comparison_cluster.jpg")

# RottenTomatoes 10 films with lowest ratings
norm_films = fandango_w_all_sites[['FILM', 'STARS', 'RATING', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm']]
output.write("16) RottenTomatoes 10 films with lowest rating\n" +
             norm_films.nsmallest(10, 'RT_Norm').to_string() + f"\n{separation}\n")

# Comparison KDE plot
# Ratings for 10 films worst rated by RottenTomatoes
plt.figure(figsize=(15, 6), dpi = 150)
worst_films = norm_films.nsmallest(10, 'RT_Norm').drop('FILM', axis = 1)
sns.kdeplot(worst_films, clip=[0,5], fill=True)
plt.title("Ratings for RT Critic's 10 Worst Reviewed Films")

plt.savefig(r"plots\10_worst_films_RT")

output.close()





