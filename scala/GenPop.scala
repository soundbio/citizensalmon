import java.io.PrintWriter
import java.util.Random
import scala.io.Source


case class ConditionalProbability(alleleCount: Long, totalPopCount: Long,
                                  subPopAlleleCount: Long, subPopTotalCount: Long) {
  def f(d: Double) = f"$d%2.4f"
  val alleleProb = alleleCount.toDouble / totalPopCount
  val subPopProb = subPopAlleleCount.toDouble / subPopTotalCount
  val totalSubPopProb = subPopTotalCount.toDouble / totalPopCount
  // p(allele | subPop) = subPopAlleleCount / subPopTotalCount
  // p(subPop | allele) = p(allele | subPop) * p(subPop) / p(allele)
  //                    = subPopAlleleCount / subPopTotalCount * (subPopTotalCount / totalPopCount) / (alleleCount / totalPopCount)
  //                    = subPopAlleleCount / alleleCount
  val predProb = subPopAlleleCount.toDouble / alleleCount
  override def toString = {
    s"p(allele) = ($alleleCount / $totalPopCount) = ${f(alleleProb)}" +
      s"\tp(allele|pop) = ($subPopAlleleCount / $subPopTotalCount) = ${f(subPopProb)}" +
      s"\tp(pop|allele) = ($subPopAlleleCount / $alleleCount) = ${f(predProb)}"
  }
}

object SimpleVector {
  implicit class RichIntMap(m1: Map[Int, Int]) {
    def +(m2: Map[Int, Int]): Map[Int, Int] = {
      m1.keySet.union(m2.keySet).foldLeft(Map.empty[Int, Int]) { case (res, key) =>
        res.updated(key, m1.getOrElse(key, 0) + m2.getOrElse(key, 0))
      }
    }
  }
}

/*
    Shamelessly stolen from Mahout's math module, which was implemented by Ted Dunning, and explained in this
    blog post: http://tdunning.blogspot.com/2008/03/surprise-and-coincidence.html
 */
object Stats {

  def xLogX(x: Long): Double = if (x == 0) 0d else x * Math.log(x)

  def entropy(elements: Long*): Double = {
    elements.foreach(e => require(e >= 0))
    val (sum, result) = elements.foldLeft((0L, 0d)) { case ((sum, res), e) =>
      (sum + e, res + xLogX(e))
    }
    xLogX(sum) - result
  }

  def llr(k11: Long, k12: Long, k21: Long, k22: Long): Double = {
    if (!(k11 >= 0 && k12 >= 0 && k21 >= 0 && k22 >= 0)) {
      throw new Exception("arg!")
    }
    val rowEntropy = entropy(k11 + k12, k21 + k22)
    val colEntropy = entropy(k11 + k21, k12 + k22)
    val matEntropy = entropy(k11, k12, k21, k22)
    if (rowEntropy + colEntropy < matEntropy) {
      0d
    } else {
      2 * (rowEntropy + colEntropy - matEntropy)
    }
  }

  def rootLLR(k11: Long, k12: Long, k21: Long, k22: Long): Double = {
    val sqrtLLR = Math.sqrt(llr(k11, k12, k21, k22))
    if (k11.toDouble / (k11 + k12) < k21.toDouble / (k21 + k22)) {
      -sqrtLLR
    } else {
      sqrtLLR
    }
  }

  def pmiFromTotals(aAndB: Long, a: Long, b: Long, total: Long) = pmi(aAndB, a - aAndB, b - aAndB, total - a - b + aAndB)

  def pmi(aAndB: Long, aAndNotB: Long, notAAndB: Long, notAAndNotB: Long): Double = {
    rootLLR(aAndB, notAAndB, aAndNotB, notAAndNotB)
  }
}


object AllelePair {
  def parse(s: String): Option[(Int, Int)] = {
    val str = s.trim
    if (str == "0000") {
      None
    } else {
      Some(str.substring(0, 2).toInt, str.substring(2, 4).toInt)
    }
  }
}

case class GenotypeVector(label: String, population: Int, alleles: Map[Int, (Int, Int)])

object FeatureVectors {
  def toFeatureVector(genotypeVector: GenotypeVector): (Int, Map[Int, Double]) =
    (genotypeVector.population, genotypeVector.alleles.toList.flatMap(featurizeAllelePair).toMap)

  def featurizeAllelePair(allele: (Int, (Int, Int))): Iterable[(Int, Double)] = {
    //
    // 2163 -> (2,4) maps to (2163 + 1 -> 1.0, 2163 + 3 -> 1.0)
    // 2055 -> (3,3) maps to (2055 + 2 -> 2.0)
    // 3022 -> (0,0) gets filtered out
    val offset = allele._1 * 4
    allele._2 match {
      case (0, 0) => List.empty
      case (x, y) if x == y => List((offset + x - 1) -> 2d)
      case (x, y) => List((offset + x - 1) -> 1d, (offset + y - 1) -> 1d)
    }
  }

  def writeSvmLight(fileName: String, vectors: List[(Int, Map[Int, Double])], seed: Long = 13L) = {
    val pw = new PrintWriter(fileName)
    val rand = new Random(seed)
    vectors.sortBy(_ => rand.nextInt()).foreach { case (label, vecMap) =>
      pw.println(label + " " + vecMap.toList.sortBy(_._1).map(x => x._1 + ":" + x._2).mkString(" "))
    }
    pw.close()
  }
}

object GenotypeVectorBuilder {
  def apply(pop: Int, str: String): GenotypeVector = {
    if (!str.contains(",")) {
      throw new Exception(str)
    }
    val Array(label, data) = str.split(",")
    val entries = data.trim.split("\t").map(_.trim).flatMap(AllelePair.parse).zipWithIndex.map(_.swap).toMap
    new GenotypeVector(label, pop, entries)
  }
}

case class SNPAllele(snpIndex: Int, allele: Int)

case class SNPAlleleCorrelation(populationId: Int, sNPAllele: SNPAllele, count: Int)

case class Population(populationId: Int, samples: List[GenotypeVector]) {
  // frequency(2145)(1) => frequency of allele 1 at SNP 2145
  def frequency(idx: Int): Map[Int, Int] = {
    samples.flatMap { sample =>
      val x = sample.alleles.get(idx)
      x.map(a => List(a._1, a._2)).getOrElse(List.empty)
    }.foldLeft(Map.empty[Int, Int]) { case (m, allele) => m.updated(allele, m.getOrElse(allele, 0) + 1) }
  }

  def frequencies: List[SNPAlleleCorrelation] = {
    val freqs = samples.head.alleles.keys.toList.flatMap { snpIdx =>
      val fr = frequency(snpIdx)
      val snpAlleleCount = fr.map { case (allele, count) =>
        SNPAlleleCorrelation(populationId, SNPAllele(snpIdx, allele), count)
      }
      snpAlleleCount
    }
    val sorted = freqs.sortBy(-_.count)
    sorted
  }
}

case class SNPDataSet(populations: List[Population]) {
  import SimpleVector.RichIntMap
  val populationMap: Map[Int, Population] = populations.map(p => (p.populationId -> p)).toMap
  val alleleCorrelations = populations.flatMap(_.frequencies)
  val popTotalCounts: Map[Int, Int] = alleleCorrelations.groupBy(_.populationId).mapValues(_.map(_.count).sum)
  val alleleCountMap: Map[(Int, Int), Int] =
    alleleCorrelations.map(a => ((a.sNPAllele.snpIndex, a.sNPAllele.allele), a)).groupBy(_._1).mapValues(_.map(_._2.count).sum)
  val totalCount = populations.map(_.samples.size).sum * 2

  val alleleLLRMap = alleleCorrelations.map { a =>
    val numInPop = populationMap(a.populationId).samples.size * 2
    val numWithAllele = alleleCountMap((a.sNPAllele.snpIndex, a.sNPAllele.allele))
    val count = a.count
    a -> Stats.pmiFromTotals(count, numInPop, numWithAllele, totalCount)
  }.toMap
  val alleleLLRs: List[(SNPAlleleCorrelation, Double)] = alleleLLRMap.toList.sortBy(-_._2)
  val alleleLLRsByPop =
    populations.map(pop => pop.populationId -> alleleLLRs.filter(_._1.populationId == pop.populationId)).toMap

  val snpAlleles: Map[Int, List[(SNPAlleleCorrelation, Double)]] = alleleLLRs.groupBy(_._1.sNPAllele.snpIndex)
  // list of (snpIndex, List[(SNPAlleleCorrelation at this snpIndex, pmi)]) pairs:
  val bestSnps: List[(Int, List[(SNPAlleleCorrelation, Double)])] = snpAlleles.toList.sortBy(-_._2.map(_._2).sum)

  def bestSnpsPretty = bestSnps.map { case (snpIndex, list) =>
    val x = list.map { case (SNPAlleleCorrelation(popId, SNPAllele(_, allele), count), llr) =>
      s"popId: $popId, snpIndex: $snpIndex, allele: $allele, llr: $llr"
    }
    x.mkString("\n")
  }

  // want to look at: given (snpIndex), what is p(popI | alleleJ) for all (popI, alleleJ) pairs, and what is p(alleleJ)
  val probs: Map[Int, Map[Int, Map[Int, List[SNPAlleleCorrelation]]]] =
    alleleCorrelations.groupBy(_.sNPAllele.snpIndex).mapValues(_.groupBy(_.populationId).mapValues(_.groupBy(_.sNPAllele.allele)))


  def conditionalProbability(popId: Int, snpIndex: Int, allele: Int): ConditionalProbability = {
    val subPopAlleleCount = alleleCounts(popId, snpIndex).getOrElse(allele, 0)
    val alleleCountTotal = aggregateAlleleCounts(snpIndex).getOrElse(allele, 0)
    ConditionalProbability(alleleCountTotal, totalCount, subPopAlleleCount, populationMap(popId).samples.size * 2)
  }

  def alleleCounts(popId: Int, snpIndex: Int) = populationMap(popId).frequency(snpIndex)
  def alleleCountsAcrossPops(snpIndex: Int): Map[Int, Map[Int, Int]] = {
    populations.map { case (Population(popId, _)) => popId -> alleleCounts(popId, snpIndex) }
  }.toMap
  def aggregateAlleleCounts(snpIndex: Int): Map[Int, Int] =
    alleleCountsAcrossPops(snpIndex).foldLeft(Map.empty[Int, Int]) { case (totals, (_, counts)) => totals + counts }

}

object SNPDataSetLoader {
  def loadPopulations(dir: String = "/Users/jakemannix/bio/hivebio/citizen_salmon",
                      file: String = "genepop_western_alaska_chinook_RAD.txt") = {
    val lines = Source.fromFile(dir + "/" + file).getLines.toList
    val (header, popLines) = (lines.take(10946), lines.drop(10946))
    val groupedLines = popLines.mkString("\n").split("Pop").map(_.split("\n").toList).zipWithIndex.toList
    val populations = groupedLines.map { case (gLines, popId) =>
      Population(popId, gLines.flatMap(line =>
        if (line.contains(",")) Some(GenotypeVectorBuilder.apply(popId, line)) else None
      ))
    }
    populations
  }
}
