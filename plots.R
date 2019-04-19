# --------------------
# Housekeeping
# --------------------

# Load packages
library(dplyr)
library(ggplot2)

# Setup plot themes
themes <- theme_bw() +
  theme(legend.title=element_blank(),
        legend.position="bottom",
        panel.grid.minor = element_blank(),
        axis.title = element_text(size=14,face="bold"),
        axis.text = element_text(size=14),
        legend.text = element_text(size=12),
        panel.border = element_blank(),
        legend.direction = "horizontal")

# --------------------
# Analysis
# --------------------

# Read data
d1 <- read.csv("./output/swn_analysis.csv",stringsAsFactors = F) %>% select(text=commentText,score) %>% arrange(-score)
d2 <- read.csv("./output/vader_analysis.csv",stringsAsFactors = F) %>% select(text=commentText,score) %>% arrange(-score)
d3 <- read.csv("./output/google_analysis.csv",stringsAsFactors = F) %>% select(text=commentText,score) %>% arrange(-score)

# Rescale SWN data
swn_max <- max(d1$score)
swn_min <- min(d1$score)
swn <- max(swn_max,-swn_min)
d1 <- d1 %>% mutate(score = score / swn * 0.9)

# Plot histograms of all results
ggplot(d1,aes(x=score)) + 
  geom_histogram(data=d1,aes(fill = "SWN (-0.01)"), alpha = 0.4,position="identity",bins=25) +
  geom_histogram(data=d2,aes(fill = "Vader (-0.01)"), alpha = 0.4,position="identity",bins=25) +
  geom_histogram(data=d3,aes(fill = "Google (-0.48)"), alpha = 0.4,position="identity",bins=25) +
  themes + xlab("Sentiment Score") + ylab("Comment Count")

ggsave("./output/histogram.png")
