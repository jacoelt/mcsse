import { Stack } from "@mui/material"
import { useState } from "react"
import TosDialog from "./TosDialog"
import PrivacyDialog from "./PrivacyDialog"
// import ContactDialog from "./ContactDialog"
// import CookiesDialog from "./CookiesDialog"
import AboutDialog from "./AboutDialog"

export default function Footer({ sx }: { sx?: React.CSSProperties }) {
  const [isTosVisible, setIsTosVisible] = useState(false)
  const [isPrivacyVisible, setIsPrivacyVisible] = useState(false)
  // const [ isCookiesVisible, setIsCookiesVisible ] = useState(false)
  // const [isContactVisible, setIsContactVisible] = useState(false)
  const [isAboutVisible, setIsAboutVisible] = useState(false)

  // const [contactSubject, setContactSubject] = useState("")


  return (
    <footer>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
        spacing={4}
        sx={{ ...sx }}
      >
        <Stack direction="column" alignItems="center">
          <a href="#" onClick={() => setIsTosVisible(true)}>Terms of Service</a>
          <a href="#" onClick={() => setIsPrivacyVisible(true)}>Privacy Policy</a>
          {/* <a href="#" onClick={() => setIsCookiesVisible(true)}>Cookie Policy</a> */}
        </Stack>
        <Stack direction="column" alignItems="center">
          Contact Us:
          <a
            href="mailto:&#099;&#111;&#110;&#116;&#097;&#099;&#116;&#046;&#109;&#105;&#110;&#101;&#099;&#114;&#097;&#102;&#116;&#115;&#101;&#114;&#118;&#101;&#114;&#101;&#120;&#112;&#108;&#111;&#114;&#101;&#114;&#064;&#103;&#109;&#097;&#105;&#108;&#046;&#099;&#111;&#109;"
            target="_blank">
            &#099;&#111;&#110;&#116;&#097;&#099;&#116;&#046;&#109;&#105;&#110;&#101;&#099;&#114;&#097;&#102;&#116;&#115;&#101;&#114;&#118;&#101;&#114;&#101;&#120;&#112;&#108;&#111;&#114;&#101;&#114;&#064;&#103;&#109;&#097;&#105;&#108;&#046;&#099;&#111;&#109;
          </a>

          <a href="#" onClick={() => setIsAboutVisible(true)}>About Us</a>
        </Stack>
      </Stack>

      <TosDialog isVisible={isTosVisible} setIsVisible={setIsTosVisible} />
      <PrivacyDialog isVisible={isPrivacyVisible} setIsVisible={setIsPrivacyVisible} />
      {/* <CookiesDialog isVisible={isCookiesVisible} setIsVisible={setIsCookiesVisible} /> */}
      {/* <ContactDialog
        isVisible={isContactVisible}
        setIsVisible={setIsContactVisible}
        initialSubject={contactSubject}
      /> */}
      <AboutDialog isVisible={isAboutVisible} setIsVisible={setIsAboutVisible} />
    </footer>
  )
}