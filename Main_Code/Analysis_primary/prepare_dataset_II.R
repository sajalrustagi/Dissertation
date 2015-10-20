library(e1071)
library(RMySQL)
library(caret) 
library("reshape2")
library("ggplot2")

# install.packages(doParallel)
library(doParallel)
cl <- makeCluster(detectCores()) 
registerDoParallel(cl)


mydb = dbConnect(MySQL(), user='root', password='sajal', dbname='Disease_names', host='localhost', passwd='sajal')
rs = dbSendQuery(mydb,'set character set "utf8"')

word_count<-1000
query=paste("SELECT * FROM `Topics_LDA_1_temp_1000` ORDER BY  `Topics_LDA_1_temp_1000`.`Probability` DESC LIMIT 0 ,",toString(word_count))
rs = dbSendQuery(mydb, query)
words = fetch(rs, n=-1)
words <- subset(words, select = -Topic_Num)

new__non_rs = dbSendQuery(mydb, "SELECT `ArticleText`,`Stemmed_Article` FROM  `Articles_English_language_Non_corpus_II` GROUP BY  `ArticleText`,`Stemmed_Article`")
non_corpus_stemmed_articles = fetch(new__non_rs, n=-1)
len_non_corpus_stemmed_articles<-length(non_corpus_stemmed_articles$Stemmed_Article)

# nondata_II_new <- as.data.frame(setNames(replicate(word_count+1,logical(len_non_corpus_stemmed_articles), simplify = F), seq(1:(word_count+1))))
# colnames(nondata_II_new)<-c(words$Word,"result")
# for(i in 1:word_count) 
# {
#   for (j in 1:len_non_corpus_stemmed_articles)
#   {
#     article= non_corpus_stemmed_articles$Stemmed_Article[j]
#     word=words$Word[i]
#     nondata_II_new[[word]][j]<-grepl(word,article)
#   }
# }
# nondata_II_new$result<-rep(c(F),each=len_non_corpus_stemmed_articles)
# save(nondata_II_new, file="nondata_II_new.saved")

library(tm)
library(SnowballC)   
docs <- Corpus(VectorSource(non_corpus_stemmed_articles$ArticleText))
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
nondata_II_corpus<-docs
save(nondata_II_corpus, file="nondata_II_corpus.saved")
