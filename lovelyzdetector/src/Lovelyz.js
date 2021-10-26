import React, {useState} from "react"

const Lovelyz = () =>{
    const [width, setWidth] = useState(400)
    const [height, setHeight] = useState(600);
    const dropAreaImageStyle = {
        width,
        height,
      };
      const borderStyle = "2px dotted #000";      
      const dropAreaStyle = {
        ...dropAreaImageStyle,
        border: borderStyle,
        justifyContent: "center",
      };


    const [data, setData] = useState(false);
    const [err, setErr] = useState(false);
    
    const [ret, setRet] = useState("")
    const [retLabel, setRetLabel] = useState("")
    const [retProb, setRetProb] = useState(0)
    
    const [retImg, setRetImg] = useState();
    const [retVisibility, setRetVisibility] = useState(false);
    const visible = ()=>{
        setRetVisibility(!retVisibility);
    }

    const onDrop = (e) => {
        e.preventDefault();
        const {
            dataTransfer: { files },
        } = e;
        const {length} = files;

        const reader = new FileReader();
        if (length === 0){
            return false;
        }
        const fileTypes = ["image/jpeg", "image/jpg", "image/png"];
        const { type } = files[0]
        
        const fileUrl = URL.createObjectURL(files[0]);
        let formdata = new FormData();
        formdata.append("fileUrl", fileUrl)
        formdata.append("file", files[0])
        fetch("/lovelyz", {
            method: "POST",
            body: formdata,
        }).then((response) =>{
            response.json().then((result)=>{
                setRet(result);
                setRetImg(result.retImg);
                setRetLabel(result.label)
                setRetProb(result.prob)
            });
        });
        setData(false);
        if (!fileTypes.includes(type)){
            return false;
        }
        setErr(false);

        reader.readAsDataURL(files[0])
        reader.onload = (loadEvt) => {
            setData(loadEvt.target.result)
        };
    };
    const onDragStart = (e) => {
        e.preventDefault();
    }
    const onDragOver = (e) => {
        e.preventDefault()
    }
    
    return (
        <div className="container">
                <div className="row">
                    <div
                        style={dropAreaStyle}
                        onDrop={(e)=>onDrop(e)}
                        onDragOver={(e)=>onDragOver(e)}
                    >
                        {data && <img style={dropAreaImageStyle} src={data}  alt=""/>}
                        {!data && <h2 style={{textAlign: "center"}}>DROP THE PHOTO HERE</h2>}
                        <div>
                            <br />
                            {data && (
                                <button
                                onClick={()=>{
                                    setData(false);
                                    setRet("")
                                    setRetImg(null);
                                }}
                                >
                                    CLEAR AND TRY NEW PHOTO
                                </button>
                            )}
                        </div>
                    </div>
                
                    <div className="col" style={{marginLeft:"10%"}}>
                    {ret ? (
                        
                        <div                         
                            style={{
                                marginBottom: "10px",
                                marginLeft:"auto",
                                marginRight: "auto",
                                testAlign: "left"}}>
                                    {retLabel} ({retProb}%)
                                <br />
                                
                                <img
                                src={`data:image/png;base64, ${retImg}`}
                                style={{
                                width: "50%",
                                marginLeft: "auto",
                                marginRight: "auto",
                                }} alt=""/>
                            </div>
                        
                    ):(            
                    <div className="col" style={{marginLeft:"10%"}}>
                    <h1>How to Use!</h1>
                    <p
                      style={{
                        marginLeft: "5%",
                        textAlign: "left",
                      }}
                    >
                      <ul style={{ lineHeight: "2rem" }}>
                        <li>
                          러블리즈 사진을 왼쪽 이미지 존에 드롭합니다.
                        </li>
                        <li>
                          현재는 사진에서 한 명의 얼굴만 확인합니다.
                        </li>
                        <li>
                          찾아진 이름과 확률이 표시됩니다.
                        </li>
                        <li>
                          탐색결과 사진은 이곳에 표현됩니다.
                        </li>
                        
                       </ul>
                    </p>
                  </div>)}
                </div>
                </div>                
        </div>
    )
};

export default Lovelyz;