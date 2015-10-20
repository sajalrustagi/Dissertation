library(e1071)
library(RMySQL)
library(caret) 
library("reshape2")
library("ggplot2")

# install.packages(doParallel)
library(doParallel)
cl <- makeCluster(20,outfile="out.txt") 
registerDoParallel(cl)


mydb = dbConnect(MySQL(), user='root', password='sajal', dbname='Disease_names', host='localhost', passwd='sajal')
rs = dbSendQuery(mydb,'set character set "utf8"')

word_count<-1000
query=paste("SELECT * FROM `Topics_LDA_1_temp_1000` ORDER BY  `Topics_LDA_1_temp_1000`.`Probability` DESC LIMIT 0 ,",toString(word_count))
rs = dbSendQuery(mydb, query)
words = fetch(rs, n=-1)
words <- subset(words, select = -Topic_Num)

new__non_rs = dbSendQuery(mydb, "SELECT `Article`,`Stemmed_Article` FROM  `Articles_English_language_corpus` GROUP BY  `Article`,`Stemmed_Article`")
corpus_stemmed_articles = fetch(new__non_rs, n=-1)
len_corpus_stemmed_articles<-length(corpus_stemmed_articles$Stemmed_Article)

nodata_new <- as.data.frame(setNames(replicate(word_count+1,logical(len_corpus_stemmed_articles), simplify = F), seq(1:(word_count+1))))
colnames(nodata_new)<-c(words$Word,"result")
#foreach(i=1:3) %dopar% sqrt(i)
i=0
for(i in 1:word_count)
#%dopar% 
{
#   Sys.sleep(0.1)
#   print(i)
  for (j in 1:len_corpus_stemmed_articles)
  {
    article= corpus_stemmed_articles$Stemmed_Article[j]
    word=words$Word[i]
    nodata_new[[word]][j]<-grepl(word,article)
  }
}
nodata_new$result<-rep(c(F),each=len_corpus_stemmed_articles)
save(nodata_new, file="nodata_new_fast.saved")

library(tm)
library(SnowballC)   
docs <- Corpus(VectorSource(corpus_stemmed_articles$Article))
docs <- tm_map(docs, removePunctuation)
for(j in seq(docs))   
{   
  docs[[j]] <- gsub("/", " ", docs[[j]])   
  docs[[j]] <- gsub("@", " ", docs[[j]])   
  docs[[j]] <- gsub("\\|", " ", docs[[j]])   
}   
docs <- tm_map(docs, tolower)   
docs <- tm_map(docs, removeWords, stopwords("english"))
docs <- tm_map(docs, stemDocument)
docs <- tm_map(docs, stripWhitespace)   
docs <- tm_map(docs, PlainTextDocument)

save(docs, file="nodata_corpus.saved")
