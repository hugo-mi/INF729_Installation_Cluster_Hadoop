# Installation d'un cluster Hadoop

## Ecosystème Hadoop

La principale motivation de l’introduction de l’écosystème Hadoop concerne la gestion des grands volumes de données. En effet, Hadoop est une plateforme open-source capable de gérer d’énormes volumes de données structurées et non structurées et ce dans le cadre d’un système distribué. L’écosystème Hadoop répond à un besoin de Google souhaitant indexer les informations texte collectait afin de présenter des résultats plus pertinents aux utilisateur de son moteur de recherche. Hadoop excelle dans le domaine de l’exécution de tâches nécessitant une grande puissance de calculs et portant sur des données volumineuses.
D’un point de vue de l’architecture, l’écosystème Hadoop a été conçu pour fonctionner sur plusieurs machines (serveurs) de manière simultanée. Chacune des machines offrent donc de la puissance de calcul et du stockage supplémentaire. Concernant le système de gestion des fichiers, les données sont éclatées sur les différentes machines et Hadoop gère un système de réplication de façon à garantir l’accès aux données à n’importe quel moment même lorsqu’une des machines tombe en panne. Concernant la distribution des calculs, la charge des traitements est répartie entre les différentes machines grâce à MapReduce. 

De manière plus concrète, l’écosystème Hadoop et composé de trois composants principaux : HDFS, MapReduce et YARN

* HDFS stocke les données (la gestion des gros volumes de données)
* MapReduce fait la magie (la gestion des calculs)
* YARN planifie tout (la gestion des ressources)

Les avantages de Hadoop sont les suivants : 
* Traitement des gros volumes de données quel que soit le format
* Mise à l’échelle facile des ressources pour le stockage et calculatoire
* Tolérance face aux pannes pour préserver l’intégrité des données
* Simplification de la manipulation des grands volumes de données

![](https://github.com/hugo-mi/INF729_Installation_Cluster_Hadoop/blob/main/Images/Ecosystem_Hadoop.jpg)

## Objectif

Mise en place d'une architecture distribuée pour la configuration d'un cluster Hadoop.

Configuration des briques logicielles suivantes :
- HDFS : Système de gestion de stockage de fichiers à tolérance de pannes.
- YARN : Allocation des ressources à chaque nœud
- Zookeeper : Synchronisation et coodination des noeuds
- Hbase : Base de données non relationnelle
- HIVE : Entreposage de données pour interroger de grands ensembles de données stockés dans le HDFS.
- Spark : Moteur de calcul distribué qui prend en charge les applications itératives tout en maintenant l'extensibilité et la tolérance aux pannes d'un cluster Hadoop.

Conception d'un programme pySpark Wordcounter qui compte les mots dans un fichier texte en tirant parti de la puissance de chaque nœud (Worker) du cluster.

Utilisation de HDFS pour stocker des fichiers volumineux.

Utilisation de Hive pour interroger de grandes bases de données

## Architecture répartie du cluster Hadoop

![](https://github.com/hugo-mi/INF729_Installation_Cluster_Hadoop/blob/main/Images/Architecture_Cluster_Hadoop.png)

## Lancement du cluster

`python3 LAUNCH.py cmdsh start`

## Arrêt du cluster

`python3 LAUNCH.py cmdsh stop`

## Commandes utiles

`jps` 
> La commande de JPS affiche tous les processus basés sur Java pour un utilisateur particulier. La commande de JPS doit s'exécuter à partir de la racine pour vérifier tous les nœuds d'exploitation de l'hôte.

`bin/hadoop dfsadmin -report`
> Affiche les informations et des statistiques du système de fichier HDFS.

`bin/hadoop fs -put <file> input`
> Peuplement du dossier `input` stocké dans HDFS

`bin/hadoop jar <app>.jar app input output `
> Lancement d'un programme java sous HDFS

## Exemple d'un programme WourdCount.java

**Compiler WordCount.java et créer un jar**
`bin/hadoop com.sun.tools.javac.Main WordCount.java`
`jar cf wc.jar WordCount*.class`

**Lancement du programme `Wordcount.java`**

`bin/hadoop jar wc.jar WordCount /user/wordcount/input /user/joe/wordcount/output`

**Afficher le résultat du programme**

`bin/hadoop fs -cat /user/wordcount/output/part-r-00000`

**Execution d'un job MapReduce avec wc.jar sur un fichier de 3.6 Go du Common-Crawl**

* [Fichier CommanCrawl](https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2017-13/segments/1490218189495.77/wet/CC-MAIN-20170322212949-00140-ip-10-233-31-227.ec2.internal.warc.wet.gz )

Output du job MapReduce

![](https://github.com/hugo-mi/INF729_Installation_Cluster_Hadoop/blob/main/Images/WC_Output_MapReduce.png)

### Création d'une table avec HIVE

**Hive **est utilisé en tant que wordcount par la création d’une nouvelle table comme suit 

`CREATE TABLE FILES (line STRING);
LOAD DATA INPATH 'input/<fichier d’input>' OVERWRITE INTO TABLE FILES;
CREATE TABLE word_counts AS
SELECT word, count(1) AS count FROM
(SELECT explode(split(line, ' ')) AS word FROM FILES) w
GROUP BY word
ORDER BY word;
`

**Affichez la sortie**

`bin/hadoop fs -cat /user/hive/warehouse/word_counts/000000_0`

![](https://github.com/hugo-mi/INF729_Installation_Cluster_Hadoop/blob/main/Images/WC_Output_Hive.png)

### Execution d'un job Wordcounter pySpark 

**Execution du programme pySpark `WC_pypsark_file_arg.py`**

`bin/spark-submit ./WC_pyspark/WC_pypsark_file_arg.py ../hadoop/data/file02`

**Execution du programme pySpark `wc.py` prenant en entré un fichier stocké dans le systège HDFS**

`bin/spark spark-submit wc.py`

**Affichage du résultat**

`bin/hadoop fs cat sparkouput/part-00000`

![](https://github.com/hugo-mi/INF729_Installation_Cluster_Hadoop/blob/main/Images/WC_Outpu2t.png)
