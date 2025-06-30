import { Stack } from "@mui/material"
import { useState } from "react"
import TosDialog from "./TosDialog"
import PrivacyDialog from "./PrivacyDialog"
import ContactDialog from "./ContactDialog"
// import CookiesDialog from "./CookiesDialog"
import AboutDialog from "./AboutDialog"

export default function Footer() {
  const [ isTosVisible, setIsTosVisible ] = useState(false)
  const [ isPrivacyVisible, setIsPrivacyVisible ] = useState(false)
  // const [ isCookiesVisible, setIsCookiesVisible ] = useState(false)
  const [ isContactVisible, setIsContactVisible ] = useState(false)
  const [ isAboutVisible, setIsAboutVisible ] = useState(false)
  const [ isReportVisible, setIsReportVisible ] = useState(false)

  const [ contactSubject, setContactSubject ] = useState("")


  return (
    <footer>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
      >
        <Stack direction="column" alignItems="center">
          <a href="#" onClick={() => setIsTosVisible(true)}>Terms of Service</a>
          <a href="#" onClick={() => setIsPrivacyVisible(true)}>Privacy Policy</a>
          {/* <a href="#" onClick={() => setIsCookiesVisible(true)}>Cookie Policy</a> */}
        </Stack>
        <Stack direction="column" alignItems="center">
          <a href="#" onClick={() => {setContactSubject(""); setIsContactVisible(true)}}>Contact Us</a>
          <a href="#" onClick={() => setIsAboutVisible(true)}>About Us</a>
        </Stack>
      </Stack>

      <TosDialog isVisible={isTosVisible} setIsVisible={setIsTosVisible} />
      <PrivacyDialog isVisible={isPrivacyVisible} setIsVisible={setIsPrivacyVisible} />
      {/* <CookiesDialog isVisible={isCookiesVisible} setIsVisible={setIsCookiesVisible} /> */}
      <ContactDialog
        isVisible={isContactVisible}
        setIsVisible={setIsContactVisible}
        initialSubject={contactSubject}
      />
      <AboutDialog isVisible={isAboutVisible} setIsVisible={setIsAboutVisible} />
    </footer>
  )
}