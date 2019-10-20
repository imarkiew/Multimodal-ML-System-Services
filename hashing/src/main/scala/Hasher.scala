import org.mindrot.jbcrypt.BCrypt
import scala.io.Source.fromFile
import java.io.PrintWriter
import scala.util.Using
import scala.util.Success


object Hasher extends App {

  val inputFilepath = args(0)
  val outputFilePath = args(1)
  val hasherFunc = (password: String) => BCrypt.hashpw(password, BCrypt.gensalt)
  val passwords = Using(fromFile(inputFilepath, "utf-8")){source => source.getLines.toSeq}

  passwords match {
    case Success(x: Seq[String]) =>
      new PrintWriter(outputFilePath){
        val hashs = x.map(hasherFunc)
        try hashs.foreach(x => write(x + "\n"))
        catch {
          case _: Exception => println("There was a problem during saving output file")
        }
        finally close()}
    case _ => println("There was a problem during reading input file")
  }
}
