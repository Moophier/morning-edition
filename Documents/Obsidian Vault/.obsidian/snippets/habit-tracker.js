async function getHabitStats(habitName) {
    const files = app.vault.getMarkdownFiles().filter(f => f.path.startsWith('00PeriodicNotes/Daily/'));
    let count = 0;
    for (const file of files) {
        const content = await app.vault.read(file);
        if (content.includes(`- [x] Habit: ${habitName}`)) count++;
    }
    return count;
}