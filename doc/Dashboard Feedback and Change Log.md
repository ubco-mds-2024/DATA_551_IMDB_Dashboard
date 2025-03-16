# Dashboard Feedback and Change Log

This document summarizes the feedback received on the dashboard along with the current status or decisions made for each item.

------------------------------------------------------------------------

## General Feedback

-   **"Impressive amount of content!"**
    -   **Status:** Positive comment. No changes required.

------------------------------------------------------------------------

## Pie Chart

-   **Comment:**\
    *"The pie chart throws an error at first because there's no default stat selected, but once I choose from the drop down it works fine."*
-   **Status:** Solved.

------------------------------------------------------------------------

## Chart Readability

-   **Comment:**\
    *"Some charts are hard to read (e.g., grossWorldWide budget scatter plot) and might benefit from a transformation, or in some cases not being included."*
-   **Status:**\
    The dashboard is intended for users to explore the data, so as many types of plots as possible are provided for exploration rather than removing charts.

------------------------------------------------------------------------

## Dashboard Layout

-   **Comment:**\
    *"The dashboard is too tall for my screen (the bottom is cut off and I need to scroll down to see the second row of plots)."*
-   **Status:**\
    Solved. 

------------------------------------------------------------------------

## Statistics Screen Layout

-   **Comment:**\
    *"On the statistics screen, I would put the Top 10 above the DataFrame Preview (or even put the DF Preview on its own tab) because it's more interesting."*
-   **Status:**\
    Solved – The layout was adjusted so that the Top 10 section now appears above the DataFrame Preview.

------------------------------------------------------------------------

## Overall Page Complexity

-   **Comment:**\
    *"Overall the first page is pretty busy and I would either split it up into multiple pages, shrink/combine the plots, or remove some altogether. Some don't really make sense like Year Bar Chart."*
-   **Status:**\
    No changes – The dashboard is designed for exploratory analysis, offering various plot types for users to interact with.

------------------------------------------------------------------------

## Initial Loading Issues

-   **Comment (Anonymous, Mar 4 at 7:25 p.m.):**\
    *"The main problem of the dashboard is that it cannot be properly loaded for the first time. There are some errors for the loading process."*
-   **Status:**\
    Solved.

------------------------------------------------------------------------

## Plot Details (Titles and Labels)

-   **Comment (Anonymous, Mar 6 at 12:01 p.m.):**\
    *"Based on the proper rendering from the second try, the format of the plots is great; however, the lack of x-labels makes it hard to understand the content. My recommendation would be to add detailed titles, axis labels, and a main title for the entire dashboard."*
-   **Status:**\
    Solved.

------------------------------------------------------------------------

## Pie Chart Tooltips

-   **Comment:**\
    *"Tooltips can be added to the pie chart."*
-   **Status:**\
    Solved.

------------------------------------------------------------------------

## Plot Arrangement

-   **Comment:**\
    *"You may arrange your plots based on the significance of the plots, not by category."*
-   **Status:**\
    Decision – The plots are intended for user exploration; therefore, all plot types are included for flexibility.

------------------------------------------------------------------------

## Variable Naming

-   **Comment:**\
    *"The dropdown options should use more official variable names (e.g., 'Movie Gross in North America' instead of 'gross_US_Canada')."*
-   **Status:**\
    Solved.

------------------------------------------------------------------------

## DataFrame Preview vs. Film Locations

-   **Comment:**\
    *"From my standpoint, the preview of the dataset is unnecessary. Instead, a map of film locations would be more interactive and appealing."*
-   **Status:**\
    Decision – Although the dataset includes a film location column, it only contains location names (without coordinates). Due to resource constraints and group size (2 vs. 4 in other groups), this feature is dropped to meet the deadline.

------------------------------------------------------------------------

