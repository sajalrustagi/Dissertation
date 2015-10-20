# install.packages("caret")
# install.packages("RMySQL")
# install.packages("e1071")

library(e1071)
library(RMySQL)
library(caret) 
library("reshape2")
library("ggplot2")
library(tm)
# install.packages(doParallel)
library(doParallel)
cl <- makeCluster(detectCores()) 
registerDoParallel(cl)

#size_training_set=30000
accuracy_size=10
accuracy_diff=100
max_to_take<-500

mydb = dbConnect(MySQL(), user='root', password='sajal', dbname='Disease_names', host='localhost', passwd='sajal')
rs = dbSendQuery(mydb,'set character set "utf8"')

# new__non_rs = dbSendQuery(mydb, "SELECT distinct Stemmed_Article FROM `Articles_English_language_Non_corpus`")
# non_corpus_stemmed_articles = fetch(new__non_rs, n=-1)
# len_non_corpus_stemmed_articles<-length(non_corpus_stemmed_articles$Stemmed_Article)
# 
# new__non_rs_II = dbSendQuery(mydb, "SELECT distinct Stemmed_Article FROM `Articles_English_language_Non_corpus_II`    where Stemmed_Article !=\"\"")
# non_corpus_stemmed_articles_II = fetch(new__non_rs_II, n=-1)
# len_non_corpus_stemmed_articles_II<-length(non_corpus_stemmed_articles_II$Stemmed_Article)
# 
# new_rs = dbSendQuery(mydb, "SELECT distinct Stemmed_Article FROM `Corpus_English`  where Stemmed_Article !=\"\"" )
# stemmed_articles = fetch(new_rs, n=-1)
# len_stemmed_article<-length(stemmed_articles$Stemmed_Article)

list_iterate_time=c(seq(10,90,10),seq(100,1000,100))
len_list_iterate_time=length(list_iterate_time)
overall_accuracy_train_total_I<-double(len_list_iterate_time)
overall_accuracy_test_total_I<-double(len_list_iterate_time)
overall_accuracy_train_total_II<-double(len_list_iterate_time)
overall_accuracy_test_total_II<-double(len_list_iterate_time)
overall_time_train_total_I<-double(len_list_iterate_time)
overall_time_test_total_I<-double(len_list_iterate_time)
overall_time_train_total_II<-double(len_list_iterate_time)
overall_time_test_total_II<-double(len_list_iterate_time)
seq_value<-double(len_list_iterate_time)
# time_train<-double(accuracy_size)
# time_test<-double(accuracy_size)





load("nodata_new_fast.saved")
load("nodata_corpus.saved")
nodata_new$result<-rep(c(T),each=nrow(nodata_new))
sampling_I<-sample(nrow(nodata_new),max_to_take)
test_x_corpus_I<-nodata_new[sampling_I,]
total<-c(1:nrow(nodata_new))
test_x_corpus_sample<-sampling_I


load("nondata_new.saved")
load("nondata_II_new.saved")
load("nondata_corpus.saved")
load("nondata_II_corpus.saved")
nondata_new<-rbind(nondata_new,nondata_II_new)
len_non_corpus<-nrow(nondata_new)
total_II<-c(1:len_non_corpus)
sampling_II<-sample(nrow(nondata_new),max_to_take)
test_x_non_corpus_I<-nondata_new[sampling_II,]
test_x_non_corpus_sample<-sampling_II

nondata_corpus_new<-c(nondata_corpus,nondata_II_corpus)
test_x_non_corpus_II<-nondata_corpus_new[sampling_II]
test_x_corpus_II<-docs[sampling_I]


#list_iterate_time=c(1:9,seq(10,90,10),seq(100,900,100),seq(1000,9000,1000),seq(10000,100000,10000))

#list_iterate_time=c(100)
count=0
for (iterate_time in list_iterate_time) 
{
  word_count<-iterate_time
  query=paste("SELECT * FROM `Topics_LDA_1_temp_1000` ORDER BY  `Topics_LDA_1_temp_1000`.`Probability` DESC LIMIT 0 ,",toString(word_count))
  rs = dbSendQuery(mydb, query)
  words = fetch(rs, n=-1)
  words <- subset(words, select = -Topic_Num)
  
  count=count+1
  size_training_set<-1250
  
  accuracy_train_I<-double(5)
  accuracy_test_I<-double(5)
  accuracy_train_II<-double(5)
  accuracy_test_II<-double(5)
  time_train_I<-double(5)
  time_test_I<-double(5)
  time_train_II<-double(5)
  time_test_II<-double(5)
  
  for (inside_iterate_time in 1:5)
  {
    train_x_corpus_sample<-sample(total[!total %in% sampling_I],size_training_set)
    train_x_non_corpus_sample<-sample(total_II[!total_II %in% sampling_II],size_training_set)
    train_x_corpus_I<-nodata_new[train_x_corpus_sample,]
    train_x_non_corpus_I<-nondata_new[train_x_non_corpus_sample,]
    
    train_x_corpus_I<-subset(train_x_corpus_I, select = c(words$Word,"result"))
    test_x_corpus_I<-subset(test_x_corpus_I, select = c(words$Word,"result"))
    train_x_non_corpus_I<-subset(train_x_non_corpus_I, select = c(words$Word,"result"))
    test_x_non_corpus_I<-subset(test_x_non_corpus_I, select = c(words$Word,"result"))
    
    x<-subset(rbind(train_x_corpus_I,train_x_non_corpus_I), select = -result)
    y<-subset(rbind(train_x_corpus_I,train_x_non_corpus_I), select = result)
    colnames(y)<-"y"
    
    start.time <- Sys.time()
    
    model <- svm(x, y,type='C-classification')
    
    end.time <- Sys.time()
    time.taken <- end.time - start.time
    time_train_I[inside_iterate_time]<-time.taken
    pred <- predict(model, x) 
    pred<-as.data.frame(pred)
    tab<-table(pred$pred,y$y)
    conf<-confusionMatrix(tab)
    accuracy_train_I[inside_iterate_time]<-conf$overall[1]
    
    
    test_x<-subset(rbind(test_x_corpus_I,test_x_non_corpus_I),select=-result)
    test_y<-subset(rbind(test_x_corpus_I,test_x_non_corpus_I),select=result)
    # test on the whole set
    start.time <- Sys.time()
    pred <- predict(model, test_x) 
    end.time <- Sys.time()
    time.taken <- end.time - start.time
    time_test_I[inside_iterate_time]<-time.taken
    
    pred<-as.data.frame(pred)
    tab<-table(pred$pred,test_y$result)
    conf<-confusionMatrix(tab)
    accuracy_test_I[inside_iterate_time]<-conf$overall[1]
    
    
    train_x_non_corpus_II<-nondata_corpus_new[train_x_non_corpus_sample]
    train_x_corpus_II<-docs[train_x_corpus_sample]
    train_x_total<-c(train_x_non_corpus_II,train_x_corpus_II)
    dtm <- DocumentTermMatrix(train_x_total)   
    dtms <- removeSparseTerms(dtm, 0.98)
    freq <- colSums(as.matrix(dtms))   
    ord <- order(freq)   
    new_words<-rev(tail(names(freq[ord]),word_count))
    
    length_train_x_non_corpus=length(train_x_non_corpus_II)
    train_x_non_corpus_II_temp <- as.data.frame(setNames(replicate(word_count+1,logical(length_train_x_non_corpus), simplify = F), seq(1:(word_count+1))))
    colnames(train_x_non_corpus_II_temp)<-c(new_words,"result")
    for(i in 1:length_train_x_non_corpus) 
    {
      train_x_non_corpus_II_temp[i,]<-c(sapply(new_words,grepl,train_x_non_corpus_II[i])[1,],F)
    }
    length_train_x_corpus=length(train_x_corpus_II)
    train_x_corpus_II_temp <- as.data.frame(setNames(replicate(word_count+1,logical(length_train_x_corpus), simplify = F), seq(1:(word_count+1))))
    colnames(train_x_corpus_II_temp)<-c(new_words,"result")
    for(i in 1:length_train_x_corpus) 
    {
      train_x_corpus_II_temp[i,]<-c(sapply(new_words,grepl,train_x_corpus_II[i])[1,],T)
    }
    train_X_II<-rbind(train_x_non_corpus_II_temp,train_x_corpus_II_temp)
    
    x<-subset(train_X_II, select = -result)
    y<-subset(train_X_II, select = result)
    colnames(y)<-"y"
    
    start.time <- Sys.time()
    
    model <- svm(x, y,type='C-classification')
    
    end.time <- Sys.time()
    time.taken <- end.time - start.time
    time_train_II[inside_iterate_time]<-time.taken
    pred <- predict(model, x) 
    pred<-as.data.frame(pred)
    tab<-table(pred$pred,y$y)
    conf<-confusionMatrix(tab)
    accuracy_train_II[inside_iterate_time]<-conf$overall[1]
    
    length_test_x_non_corpus=length(test_x_non_corpus_II)
    test_x_non_corpus_II_temp <- as.data.frame(setNames(replicate(word_count+1,logical(length_test_x_non_corpus), simplify = F), seq(1:(word_count+1))))
    colnames(test_x_non_corpus_II_temp)<-c(new_words,"result")
    for(i in 1:length_test_x_non_corpus) 
    {
      test_x_non_corpus_II_temp[i,]<-c(sapply(new_words,grepl,test_x_non_corpus_II[i])[1,],F)
    }
    length_test_x_corpus=length(test_x_corpus_II)
    test_x_corpus_II_temp <- as.data.frame(setNames(replicate(word_count+1,logical(length_test_x_corpus), simplify = F), seq(1:(word_count+1))))
    colnames(test_x_corpus_II_temp)<-c(new_words,"result")
    for(i in 1:length_test_x_corpus) 
    {
      test_x_corpus_II_temp[i,]<-c(sapply(new_words,grepl,train_x_corpus_II[i])[1,],T)
    }
    test_X_II<-rbind(test_x_non_corpus_II_temp,test_x_corpus_II_temp)
    
    test_x<-subset(test_X_II, select = -result)
    test_y<-subset(test_X_II, select = result)
    colnames(test_y)<-"y"
    
    start.time <- Sys.time()
    pred <- predict(model, test_x) #create predictions
    end.time <- Sys.time()
    time.taken <- end.time - start.time
    time_test_II[inside_iterate_time]<-time.taken
    
    pred<-as.data.frame(pred)
    tab<-table(pred$pred,test_y$y)
    conf<-confusionMatrix(tab)
    accuracy_test_II[inside_iterate_time]<-conf$overall[1]
    
  }
  overall_accuracy_train_total_I[count]<-mean(accuracy_train_I)
  overall_accuracy_test_total_I[count]<-mean(accuracy_test_I)
  overall_accuracy_train_total_II[count]<-mean(accuracy_train_II)
  overall_accuracy_test_total_II[count]<-mean(accuracy_test_II)
  overall_time_train_total_I[count]<-mean(time_train_I)
  overall_time_test_total_I[count]<-mean(time_test_I)
  overall_time_train_total_II[count]<-mean(time_train_II)
  overall_time_test_total_II[count]<-mean(time_test_II)
  seq_value[count]<-iterate_time
  
  
}