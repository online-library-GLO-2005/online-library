import {useLocation} from "react-router-dom";

function BookReader() {
  const {state} = useLocation();
  const pdfUrl = state?.url;

  return (
      <iframe src={pdfUrl} className="w-full h-screen"/>
  );
}

export default BookReader;
