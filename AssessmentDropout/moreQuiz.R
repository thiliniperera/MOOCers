#read file
newTrainData <- read.csv("E:/My Documents/1.ENGI/Semester 8/FYP/EDUC115/Education_EDUC115-S_Spring2014_ActivityGrade.csv")
finalData <- read.csv("E:/My Documents/1.ENGI/Semester 8/FYP/EDUC115/Education_EDUC115-S_Spring2014_FinalGrade.csv")
summary(finalData)

lastTime <- as.POSIXct((newTrainData$X.last_submit.), format="%m/%d/%Y %H:%M")
firstTime <- as.POSIXct((newTrainData$X.first_submit.), format="%m/%d/%Y %H:%M")
diff <- difftime(lastTime,firstTime,unit="mins")
duration <- c(diff)
newTrainData$duration <- duration
summary(newTrainData)
dat <- data.frame(as.numeric(as.character(duration)))
scaled.duration <- scale(dat,center = FALSE, scale = max(dat) - min(dat))
newTrainData$ScaledDuration <- scaled.duration

#remove unwanted columns
newdata <- subset(newTrainData,newTrainData$X.module_type.=="problem" & newTrainData$anon_screen_name.!="None" & newTrainData$resource_display_name.=="Quiz - Brain Growth")
#newDataSet <- subset(newdata,select = c("activity_grade_id.","student_id.", "X.module_type.","anon_screen_name.","resource_display_name.","X.first_submit.","X.last_submit.","X.grade."))

newDataSetVideo <- subset(newTrainData,newTrainData$X.module_type.=="video" & newTrainData$anon_screen_name.!="None")
#newDataSetVideo <- subset(newdataexVideo,select = c("activity_grade_id.","student_id.", "X.module_type.","anon_screen_name.","resource_display_name.","X.first_submit.","X.last_submit.","X.grade."))
summary(newDataSetVideo)

#combine video
totalSet <- merge(newdata,newDataSetVideo,by="anon_screen_name.")
totalSet$videoWatch <- ifelse(totalSet$resource_display_name..y=="Video - Brain Growth",1,0) 
summary(totalSet)
#totalsetQ1 <- subset(totalSet,totalSet$resource_display_name..y=="Video - Brain Growth")
totalsetWithFgrade <- merge(totalSet,finalData,by="anon_screen_name.")
summary(totalsetWithFgrade)
#plot(totalSet) 

#preprocess
#Create test data and training data
half <- round(nrow(totalsetWithFgrade)/2)

train1 <- totalsetWithFgrade[1:half,]
test1 <- totalsetWithFgrade[nrow(totalsetWithFgrade)- half:nrow(totalsetWithFgrade),]
library(neuralnet)

nn=neuralnet(grade.~videoWatch+X.grade..x+X.num_attempts..x+ScaledDuration.x,train1,hidden=2,err.fct = "sse",linear.output = FALSE)
nn
plot(nn)
nn$weights
nn_backProp=neuralnet(grade.~videoWatch+X.grade..x+X.num_attempts..x+ScaledDuration.x,train1,hidden=2,learningrate = 0.01,algorithm = "backprop",err.fct = "sse",linear.output = FALSE)
nn_backProp
plot(nn_backProp)

#results
results_grade <- compute(nn, covariate = matrix(c(test1$videoWatch,test1$X.grade..x,test1$X.num_attempts..x,test1$ScaledDuration.x),byrow = TRUE,ncol = 4))
results_grade$net.result
plot(results_grade$net.result)

predict_nn <- results_grade$net.result*(max(totalsetWithFgrade$grade.)-min(totalsetWithFgrade$grade.))+min(totalsetWithFgrade$grade.)
predict_nn
test_results <- test1$grade.*(max(totalsetWithFgrade$grade.)-min(totalsetWithFgrade$grade.))+min(totalsetWithFgrade$grade.)
test_results

MSE <- sum((test_results - predict_nn)^2)/nrow(test1)
MSE

#results from back propagation
results_grade_prop <- compute(nn_backProp, covariate = matrix(c(test1$videoWatch,test1$X.grade..x,test1$X.num_attempts..x,test1$ScaledDuration.x),byrow = TRUE,ncol = 4))
results_grade_prop$net.result
plot(results_grade_prop$net.result)

predict_nn_prop <- results_grade_prop$net.result*(max(totalsetWithFgrade$grade.)-min(totalsetWithFgrade$grade.))+min(totalsetWithFgrade$grade.)
predict_nn_prop


MSE <- sum((test_results - predict_nn_prop)^2)/nrow(test1)
MSE

#false negative
#3 quizes

