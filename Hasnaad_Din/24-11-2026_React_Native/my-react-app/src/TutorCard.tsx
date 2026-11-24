type TutorCardProps = {
  name: string
  subject: "Backend" | "Frontend"
  gender: "male" | "female"
  email : string
}

function TutorCard(props: TutorCardProps) {
  return (
    <div style={{ border: "1px solid grey", borderRadius: "8px", padding: "10px" }}>
      <p style={{ fontSize: "60px", margin: 0 }}>
        {props.gender === "male" ? "👨‍🏫" : "👩‍🏫"}
      </p>
      <h3>{props.name}</h3>
      <p><strong>Tutor</strong></p>
      <p>Subject: {props.subject}</p>
      <p>Email: {props.email}</p>
    </div>
  )
}

export default TutorCard