# 🏠 Home

<div class="ivy-dashboard-grid">
  <div class="ivy-dashboard-column">
    ## 📊 Statistics
    ```dataview
    LIST count(rows)
    FROM "01Projects"
    GROUP BY "Projects"
    ```
    ```dataview
    LIST count(rows)
    FROM "03Resources/Reading"
    GROUP BY "Reading"
    ```
    ```dataview
    LIST count(rows)
    FROM "03Resources/Knowledge"
    GROUP BY "Knowledge"
    ```

    ## 📅 Important Dates
    ```dataview
    LIST FROM "00PeriodicNotes/ImportantDates.md"
    WHERE date >= date(today)
    ```
  </div>

  <div class="ivy-dashboard-column">
    ## 🧭 Navigation
    - [[00PeriodicNotes|📅 Periodic Notes]]
    - [[01Projects|🚀 Projects]]
    - [[02Areas|🌐 Areas]]
    - [[03Resources|📚 Resources]]
    - [[04Archives|📦 Archives]]

    ## 🕒 Recent Activity
    ```dataview
    LIST FROM "" SORT file.mday DESC LIMIT 10
    ```
  </div>

  <div class="ivy-dashboard-column">
    ## ✅ Pending Tasks
    ```tasks
    not done
    (due before tomorrow) OR (no due date)
    ```
  </div>
</div>
