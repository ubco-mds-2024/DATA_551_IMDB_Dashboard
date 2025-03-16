Our dashboard has reached several key milestones and now consists of multiple integrated components that provide a comprehensive view of the dataset as well as predictive capabilities. The primary features that have been implemented so far include:

1. **Interactive Visualization Tabs:**  
   We have developed three primary tabs – Plots, Statistics, and Predictions – each offering different functionalities. The Plots tab includes a range of interactive visualizations such as scatter plots, line plots, histograms, bar charts, box plots, and pie charts. Each plot has been enhanced with friendly naming conventions (for instance, "Movie Gross in North America" instead of raw variable names) and tooltips for better data exploration. Additionally, we addressed earlier sizing issues: all plots are now consistently sized for better alignment and user experience.

2. **Statistics Tab:**  
   The Statistics tab displays both a "Top 10 by Average Rating" chart and a data table preview of the underlying dataset. This dual view allows users to not only visually inspect the performance metrics for different categories (such as writers, directors, or stars) but also verify the raw data in a paginated table format. We have implemented filtering by genre and minimum number of works, which helps in focusing on reliable statistics and minimizing noise from infrequent entries.

3. **Predictions Tab:**  
   In the Predictions tab, users can input parameters such as genre, star, director, and budget to predict profitability. The app uses pre-trained Random Forest models (both classification and regression) to provide an estimated profitability category as well as a predicted gross-to-budget ratio. The interface is designed to be simple and intuitive, encouraging users to explore different scenarios.

### What Is Not Yet Implemented

Despite the progress, there remain several features that are still in development or deferred due to resource constraints:

- **Advanced Filtering and Data Drill-Down:**  
  While basic filtering is implemented, advanced interactive filters (such as multi-select or dynamic drill-down capabilities for sub-categories) are not yet available. We plan to enhance this feature in a future iteration, but given the current timeline and resource constraints, we have prioritized core functionalities.

- **Performance Optimization:**  
  Although we addressed initial memory and sizing issues, the dashboard’s performance can still be improved, particularly when working with larger datasets. Feedback indicated that loading times could be optimized further, and we plan to implement more efficient data handling and caching strategies in subsequent updates.

- **User Feedback and Accessibility Improvements:**  
  Our initial testing with peers and TAs highlighted some areas for improvement in terms of ease-of-use and navigation. While we have made several UI enhancements (such as using friendly names and consistent sizing), some accessibility features and a more robust error-handling mechanism are not yet fully implemented. We value the feedback on these aspects and have noted them for future revisions.

### Feedback Summary

Feedback from our peers and TAs has been immensely valuable. Users found the dashboard intuitive and appreciated the clear visualizations and organized layout. However, there was consistent feedback regarding the speed of loading and the need for more granular filtering options. We have addressed the sizing issue and improved visual consistency, but further optimizations for performance and accessibility will be our focus moving forward.