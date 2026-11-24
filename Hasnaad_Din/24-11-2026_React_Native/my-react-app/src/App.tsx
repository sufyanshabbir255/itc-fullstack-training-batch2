import StudentCard from './StudentCard.tsx'
import TutorCard from './TutorCard.tsx'

function App() {
  return (
    <div>
    <h2>Meet the Python team</h2>
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px" }}>
      <StudentCard name="Hasnaad" course="Python Full Stack" gender="male" start_date={new Date("2026-11-03")} email="hasnaad@example.com" />
      <StudentCard name="Naba" course="Python Full Stack" gender="female" start_date={new Date("2026-11-03")} email="naba@example.com" />
      <StudentCard name="Daniel" course="Python Full Stack" gender="male" start_date={new Date("2026-11-03")} email="daniel@example.com" />
      <StudentCard name="Sauma" course="Python Full Stack" gender="female" start_date={new Date("2026-11-03")} email="sauma@example.com" />
      <TutorCard name="Romesh Bansal" subject="Backend" gender="male" email="romesh@example.com" />
      <TutorCard name="Muhammad Sufyan" subject="Frontend" gender="male" email="sufyan@example.com" />
    </div>
    </div>
  )
}

export default App