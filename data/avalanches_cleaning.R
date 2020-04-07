library(dplyr)
library(readr)
library(lubridate)
library(stringr)
library(ggplot2)

# Read in data
ava <- read_csv('avalanches_all.csv')
names(ava)[2] <- 'Area'

# Remove the rows that aren't really observations OR don't have a date
ava2 <- ava %>%
  filter(Date != 'Date') # This also removes obs without dates

# Filter out any observations before 2000
dates <- mdy(ava2$Date)
relevant_dates <- dates > mdy('01/01/2000')
ava2 <- ava2[relevant_dates,]

# Observations per region
ava2 %>%
  group_by(Region) %>%
  count() %>%
  arrange(desc(n))
# Salt Lake Region has significantly more information than any other place
# Filtering to only Salt Lake region
ava2 <- ava2 %>%
  filter(Region=='Salt Lake')

colSums(is.na(ava2))
# 118 missing values for Area, consider dropping
# 105 missing for Trigger; UNIMPORTANT, drop feature later
# 710 missing for Depth, consider dropping
# 585 missing for Width, consider dropping

# DROPPING observations missing Area data
ava2 <- ava2[!is.na(ava2$Area),]

no_depth_width <- is.na(ava2$Depth) & is.na(ava2$Width)
sum(no_depth_width)
# 443 missing any depth/width data, DROPPING
ava2 <- ava2[!no_depth_width,]

# DECIDING THAT AVALANCHE SEVERITY CANNOT BE DETERMINED
# WITHOUT KNOWING BOTH DEPTH AND WIDTH, DROPPING
# 235 missing Depth and 107 missing Width
depth_and_width <- !is.na(ava2$Depth) & !is.na(ava2$Width)
ava2 <- ava2[depth_and_width,]

# filtering out redundant Region and unnecessary Trigger features
ava2 <- ava2 %>%
  select(Date, Area, Depth, Width)

colSums(is.na(ava2))
nrow(ava2)
# Now have 1822 observations with Date, Area, Depth, and Width values

#Convert all depth/width measurements to feet
string_to_feet <- function(x) {
  if (str_detect(x, '\"')) {
    x <- str_extract(x, '([0-9]+,)*[0-9]+(\\.[0-9]+)*(?=\")')
    x <- gsub(',', '', x)
    x <- as.numeric(x)/12
  } else if(str_detect(x, '\'')) {
    x <- str_extract(x, '([0-9]+,)*[0-9]+(\\.[0-9]+)*(?=\')')
    x <- gsub(',', '', x)
  }
  return(as.numeric(x))
}
depth_feet <- sapply(ava2$Depth, string_to_feet)
width_feet <- sapply(ava2$Width, string_to_feet)

ava2$Depth <- depth_feet
ava2$Width <- width_feet

# Guesstimates from Greg of dangerous avalanches, a weather forecaster from the Utah Avalanche Center
# He reasons that an avalanche deeper than 1 ft and wider than 60 ft will run for at least 100 ft
# and could bury or injure someone
deep_enough <- ava2$Depth >= 1
wide_enough <- ava2$Width >= 60
sum(deep_enough & wide_enough)
# There are 874 (about half) of all observations that could be considered dangerous by Greg's estimates

ava2 <- ava2 %>%
  mutate(Dangerous = (Depth >= 1 & Width >= 60))

# Saving new, cleaned avalanche data
write_csv(ava2, 'avalanches_slc_clean_allareas.csv')
