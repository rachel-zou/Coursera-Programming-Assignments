library(CSeqpat)

review <- read.csv(file="C:/reviews_sample.txt", header=FALSE)

s = ""

for (row in 1:nrow(review)) {
  sen <- review[row, "V1"]
  s <- paste(s,sen,sep=",")
}

tf <- tempfile()
writeLines(s, tf)

df <- CSeqpat(tf,1,99999,100,",",FALSE,FALSE,FALSE,FALSE)

write.csv(df,'C:/patterns.txt')
