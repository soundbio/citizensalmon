##Citizen Salmon!

### Setup Instructions

First, install `virtualenvwrapper` (might require sudo):
```
$ pip install virtualenvwrapper
```

Then, add the following three lines to your shell startup file (either `~/.bashrc`, or `~/.profile`)
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Open a new terminal (or `source ~/.bashrc`) to reload wherever you added the three lines.

Now you have virtualenvwrapper installed and you can create python virtual environments!

Create a virtualenvironment for citizen salmon and install the project requirements
```
$ mkvirtualenv salmon
$ pip install -r requirements.txt
```

Now you're ready to salmon!

Whenever you want to work on the project, do:
```
$ workon salmon
```

---

To play with some statistics, in scala, there is also a small collection of functions in the scala directory.  To use, you need to make sure you install scala:

```
$ brew install scala
```

and then in this directory, you can fire up the scala REPL (with enough RAM to handle this data set) by:

```
$ scala -J-Xmx4g
```

(you can change "4g" to be "2g", or "1024m" or "12g" etc)

from there, you can play like so (lines starting with "scala>" are where you are typing - the other lines are what the REPL will respond to you):

```
$ scala -J-Xmx4g
Welcome to Scala version 2.11.7 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_66).
Type in expressions to have them evaluated.
Type :help for more information.

scala> :load scala/GenPop.scala
Loading scala/GenPop.scala...
import java.io.PrintWriter
import java.util.Random
import scala.io.Source
defined class ConditionalProbability
defined object SimpleVector
defined object Stats
defined object AllelePair
defined class GenotypeVector
defined object FeatureVectors
defined object GenotypeVectorBuilder
defined class SNPAllele
defined class SNPAlleleCorrelation
defined class Population
defined class SNPDataSet
defined object SNPDataSetLoader

scala> val data = SNPDataSetLoader.load()
data: SNPDataSet = SNPDataSet(List(Population(0,List(GenotypeVector(Koktuli10_0002,0,Map(2163 -> (3,3), 8607 -> (3,3), ...
```

At this point, any time you have a handle on a variable in scala in the REPL, you can use tab-autocompletion to see what methods are available:
```
scala> data.
aggregateAlleleCounts   alleleCountsAcrossPops   asInstanceOf     conditionalProbability   populationMap   productElement    toString     
alleleCorrelations      alleleLLRMap             bestSnps         copy                     populations     productIterator   totalCount   
alleleCountMap          alleleLLRs               bestSnpsPretty   isInstanceOf             probs           productPrefix                  
alleleCounts            alleleLLRsByPop          canEqual         popTotalCounts           productArity    snpAlleles   
```

You won't be able to tell which of these are methods, and which are instance member variables, but if you start typing one of them, tab again, let it autocomplete, if you tab twice, it'll tell you whether it's just a value you'll retrieve, or a method you can call (and what the argument types are to the method):

```
scala> data.conditionalProbability
   def conditionalProbability(popId: Int, snpIndex: Int, allele: Int): ConditionalProbability

scala> val allelesByPop = data.alleleLLRsByPop
allelesByPop: scala.collection.immutable.Map[Int,List[(SNPAlleleCorrelation, Double)]] = Map(0 -> List((SNPAlleleCorrelation(0,SNPAllele(8617,2),56),5.537387281615647), ...

scala> allelesByPop(0).take(5).foreach(println)
(SNPAlleleCorrelation(0,SNPAllele(8617,2),56),5.537387281615647)
(SNPAlleleCorrelation(0,SNPAllele(4104,1),51),5.43850921580328)
(SNPAlleleCorrelation(0,SNPAllele(1171,1),44),5.421939135648476)
(SNPAlleleCorrelation(0,SNPAllele(6262,4),52),5.316027764628513)
(SNPAlleleCorrelation(0,SNPAllele(2402,2),60),5.29338330641602)

scala> data.conditionalProbability(popId = 0, snpIndex = 8617, allele = 2)
res3: ConditionalProbability = p(allele) = (150 / 530) = 0.2830	p(allele|pop) = (56 / 112) = 0.5000	p(pop|allele) = (56 / 150) = 0.3733
```
