#read file
newTrainData <- read.csv("E:/My Documents/1.ENGI/Semester 8/FYP/EDUC115/Education_EDUC115-S_Spring2014_ActivityGrade.csv")
finalData <- read.csv("E:/My Documents/1.ENGI/Semester 8/FYP/EDUC115/Education_EDUC115-S_Spring2014_FinalGrade.csv")
summary(newTrainData)

#Calculate duration
lastTime <- as.POSIXct((newTrainData$X.last_submit.), format="%m/%d/%Y %H:%M")
firstTime <- as.POSIXct((newTrainData$X.first_submit.), format="%m/%d/%Y %H:%M")
diff <- difftime(lastTime,firstTime,unit="mins")
duration <- c(diff)
newTrainData$duration <- duration
summary(newTrainData)  #with duration
dat <- data.frame(scaledDuration = as.numeric(as.character(duration)))
scaled.duration <- scale(dat,center = FALSE, scale = max(dat) - min(dat))
newTrainData$ScaledDuration <- scaled.duration

#Add final Grade
dropout <- ifelse(tempGrade > 0, 1, 0)
finalData$dropout <- dropout
newTrainData <- merge(newTrainData,finalData,by="anon_screen_name.")
summary(newTrainData)

#remove unwanted columns
newdata_withQuizBrainGrowth <- subset(newTrainData,newTrainData$X.module_type.=="problem" & newTrainData$anon_screen_name.!="None" & newTrainData$resource_display_name.=="Quiz - Brain Growth")
newdata_withQuizBrainGrowth <- unique(newdata_withQuizBrainGrowth)
newdata_withQuizMathMythsandtheBrain <- subset(newTrainData,newTrainData$X.module_type.=="problem" & newTrainData$anon_screen_name.!="None" & newTrainData$resource_display_name.=="Quiz - Math Myths and the Brain")
newdata_withQuizHowDoPeopleFeelaboutMath <- subset(newTrainData,newTrainData$X.module_type.=="problem" & newTrainData$anon_screen_name.!="None" & newTrainData$resource_display_name.=="Quiz - How Do People Feel about Math?")
newdata_withQuizMathandHipHop <- subset(newTrainData,newTrainData$X.module_type.=="problem" & newTrainData$anon_screen_name.!="None" & newTrainData$resource_display_name.=="Quiz - Math and Hip-Hop")


newDataSetVideo <- subset(newTrainData,newTrainData$X.module_type.=="video" & newTrainData$anon_screen_name.!="None")
newDataSetVideo <- subset(newDataSetVideo,select = c("student_id.", "X.module_type.","anon_screen_name.","resource_display_name."))
summary(newDataSetVideo)

#combine video
newDataSetVideoq1 <- subset(newDataSetVideo,newDataSetVideo$resource_display_name.=="Video - Brain Growth")
totalSet_withQuiz1 <- merge(x = newdata_withQuizBrainGrowth,newDataSetVideoq1,by="anon_screen_name.",all.x = TRUE)
totalSet_withQuiz1$videoWatch <- ifelse(totalSet_withQuiz1$resource_display_name..y=="Video - Brain Growth",1,0) 

totalSet_withQuiz1<-unique(totalSet_withQuiz1)
totalSet_withQuiz1
totalSet_withQuiz1[is.na(totalSet_withQuiz1)]<-0
summary(totalSet_withQuiz1)

#plot(totalSet) 

#preprocess
#Create test data and training data
half <- round(nrow(totalSet_withQuiz1)/2)
train1 <- totalSet_withQuiz1[1:half,]
summary(train1)
test1 <- totalSet_withQuiz1[nrow(totalSet_withQuiz1)- half:nrow(totalSet_withQuiz1),]
library(neuralnet)

nn=neuralnet(grade.~videoWatch+ X.grade.+X.num_attempts.+train1$ScaledDuration,train1,hidden=2,err.fct = "sse",linear.output = FALSE)
nn
plot(nn)
nn$weights


#results_q1
results_grade <- compute(nn, covariate = matrix(c(test1$videoWatch,test1$X.grade.,test1$X.num_attempts.,test1$ScaledDuration),byrow = TRUE,ncol = 4))
results_grade$net.result
result_table <- data.frame(student = test1$anon_screen_name.,actual = test1$grade., prediction_Q1 = results_grade$net.result)
result_table_Q1<-unique(result_table)
plot(results_grade$net.result)


#quiz 2****************************************************************************
#combine video
newDataSetVideoq2 <- subset(newDataSetVideo,newDataSetVideo$resource_display_name.=="Video - Math Myths and the Brain")
totalSet_withQuiz2 <- merge(x=newdata_withQuizMathMythsandtheBrain,newDataSetVideoq2,by="anon_screen_name.",all.x = TRUE)
totalSet_withQuiz2$videoWatch <- ifelse(totalSet_withQuiz2$resource_display_name..y=="Video - Math Myths and the Brain",1,0) 
totalSet_withQuiz2<-unique(totalSet_withQuiz2)
totalSet_withQuiz2[is.na(totalSet_withQuiz2)]<-0
summary(totalSet_withQuiz2)

#preprocess
#Create test data and training data
half <- round(nrow(totalSet_withQuiz2)/2)

train2 <- totalSet_withQuiz2[1:half,]
summary(train2)
test2 <- totalSet_withQuiz2[nrow(totalSet_withQuiz2)- half:nrow(totalSet_withQuiz2),]
library(neuralnet)

nn=neuralnet(grade.~videoWatch+ X.grade.+X.num_attempts.+train2$ScaledDuration,train2,hidden=2,err.fct = "sse",linear.output = FALSE)
nn
plot(nn)
nn$weights

#results_q2
results_grade2 <- compute(nn, covariate = matrix(c(test2$videoWatch,test2$X.grade.,test2$X.num_attempts.,test2$ScaledDuration),byrow = TRUE,ncol = 4))
results_grade2$net.result
result_table2 <- data.frame(student = test2$anon_screen_name.,actual = test2$grade., prediction_Q2 = results_grade2$net.result)
result_table_Q2<-unique(result_table2)
plot(results_grade2$net.result)


#quiz 3****************************************************************************
#combine video
newDataSetVideoq3 <- subset(newDataSetVideo,newDataSetVideo$resource_display_name.=="Video - How Do People Feel about Math?")
totalSet_withQuiz3 <- merge(x=newdata_withQuizHowDoPeopleFeelaboutMath,newDataSetVideoq3,by="anon_screen_name.",all.x = TRUE)
totalSet_withQuiz3$videoWatch <- ifelse(totalSet_withQuiz3$resource_display_name..y=="Video - How Do People Feel about Math?",1,0) 
totalSet_withQuiz3<-unique(totalSet_withQuiz3)
totalSet_withQuiz3[is.na(totalSet_withQuiz3)]<-0
summary(totalSet_withQuiz3)

#preprocess
#Create test data and training data
half <- round(nrow(totalSet_withQuiz3)/2)

train3 <- totalSet_withQuiz3[1:half,]
summary(train3)
test3 <- totalSet_withQuiz3[nrow(totalSet_withQuiz3)- half:nrow(totalSet_withQuiz3),]
library(neuralnet)

nn=neuralnet(grade.~videoWatch+ X.grade.+X.num_attempts.+train3$ScaledDuration,train3,hidden=2,err.fct = "sse",linear.output = FALSE)
nn
plot(nn)
nn$weights

#results_q2
results_grade3 <- compute(nn, covariate = matrix(c(test3$videoWatch,test3$X.grade.,test3$X.num_attempts.,test3$ScaledDuration),byrow = TRUE,ncol = 4))
results_grade3$net.result
result_table3 <- data.frame(student = test3$anon_screen_name.,actual = test3$grade., prediction_Q3 = results_grade3$net.result)
result_table_Q3<-unique(result_table3)
plot(results_grade3$net.result)


#quiz 4****************************************************************************
#combine video
newDataSetVideoq4 <- subset(newDataSetVideo,newDataSetVideo$resource_display_name.=="Video - Math and Hip-Hop")
totalSet_withQuiz4 <- merge(x=newdata_withQuizMathandHipHop,newDataSetVideoq4,by="anon_screen_name.",all.x = TRUE)
totalSet_withQuiz4$videoWatch <- ifelse(totalSet_withQuiz4$resource_display_name..y=="Video - Math and Hip-Hop",1,0) 
totalSet_withQuiz4<-unique(totalSet_withQuiz4)
totalSet_withQuiz4[is.na(totalSet_withQuiz4)]<-0

summary(totalSet_withQuiz4)

#preprocess

#Create test data and training data

half <- round(nrow(totalSet_withQuiz4)/2)

train4 <- totalSet_withQuiz4[1:half,]
summary(train4)
test4 <- totalSet_withQuiz4[nrow(totalSet_withQuiz4)- half:nrow(totalSet_withQuiz4),]
library(neuralnet)

nn=neuralnet(grade.~videoWatch+ X.grade.+X.num_attempts.+train4$ScaledDuration,train4,hidden=2,err.fct = "sse",linear.output = FALSE)
nn
plot(nn)
nn$weights



#results_q2
results_grade4 <- compute(nn, covariate = matrix(c(test4$videoWatch,test4$X.grade.,test4$X.num_attempts.,test4$ScaledDuration),byrow = TRUE,ncol = 4))
results_grade4$net.result
result_table4 <- data.frame(student = test4$anon_screen_name.,actual = test4$grade., prediction_Q4 = results_grade4$net.result)
result_table_Q4<-unique(result_table4)
plot(results_grade4$net.result)


#merge result tables
result_table_total <- merge(x=result_table_Q1,result_table_Q2,all.x = TRUE)
result_table_total <- merge(x=result_table_total,result_table_Q3,all.x = TRUE)
result_table_total <- merge(x=result_table_total,result_table_Q4,all.x = TRUE)
result_table_total <- unique(result_table_total)
result_table_total[is.na(result_table_total)]<-0

nrow(result_table_total[result_table_total$actual==0.00,])

half <- round(nrow(result_table_total)/2)
train_result <- result_table_total[1:half,]
summary(train_result)
test_result <- result_table_total[nrow(result_table_total)- half:nrow(result_table_total),]

library(neuralnet)
result_nn=neuralnet(train_result$actual~train_result$prediction_Q1+train_result$prediction_Q2+train_result$prediction_Q3+train_result$prediction_Q4,train_result,hidden=2,err.fct = "sse",linear.output = FALSE)
result_nn
plot(result_nn)
result_nn$weights

#result
results_grade_all <- compute(result_nn, covariate = matrix(c(test_result$prediction_Q1,test_result$prediction_Q2,test_result$prediction_Q3,test_result$prediction_Q4),byrow = TRUE,ncol = 4))
results_grade_all$net.result
plot(results_grade4$net.result)


#Calculate Error
predict_nn <- results_grade_all$net.result*(max(result_table_total$actual)-min(result_table_total$actual))+min(result_table_total$actual)
predict_nn
test_results <- test_result$actual*(max(result_table_total$actual)-min(result_table_total$actual))+min(result_table_total$actual)
test_results

MSE <- sum((test_results - predict_nn)^2)/nrow(test_result)
MSE

