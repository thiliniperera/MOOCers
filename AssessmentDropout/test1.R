#read Data
train <- read.csv("Education_EDUC115-S_Spring2014_ActivityGrade.csv")
summary(train)

#remove unwanted columns
newdata <- subset(newTrainData,newTrainData$X.module_type.=="problem" & newTrainData$X.anon_screen_name.!="None" & newTrainData$X.resource_display_name.=="Quiz - Lesson 1")
newTrainData <- subset(train,select = c("X.activity_grade_id.","X.student_id.", "X.module_type.","X.anon_screen_name.","X.resource_display_name.","X.first_submit.","X.last_submit.","X.grade."))

#Create test data and training data
half <- round(nrow(newdata)/2)

train1 <- newdata[1:half,]
test1 <- newdata[nrow(newdata)- half:nrow(newdata),]

xd = 

#Range1 <-  as.Date(as.character(train1$X.last_submit.),format="%Y/%m/%d")- 
  #as.Date(as.character(train1$X.first_submit.),format="%Y/%m/%d")

#Range1
  
x <- as.POSIXct((train1$X.last_submit.), format="%Y-%m-%Y  %H:%M:%S")
x



