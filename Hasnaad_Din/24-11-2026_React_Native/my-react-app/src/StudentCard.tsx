type StudentCardProps = {
  name: string
  course: string
  gender: "male" | "female"
  start_date : Date
  email : string
}

function StudentCard(props: StudentCardProps) {
  return (
    <div style={{ border: "1px solid grey", borderRadius: "8px", padding: "10px" }}>
      <p style={{ fontSize: "60px", margin: 0 }}>
        {props.gender === "male" ? "👨" : "👩"}
      </p>
      <h3>{props.name}</h3>
      <p><strong>Student</strong></p>
      <p>Course: {props.course}</p>
      <p>Start date: {props.start_date.toLocaleDateString("en-GB", { month: "long", year: "numeric" })}</p>
      <p>Email: {props.email}</p>
    </div>
  )
}

export default StudentCard