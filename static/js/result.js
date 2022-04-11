var jsonData = '';

$(document).ready(function(){
    jsonData = JSON.parse([$('.verification-data').text()]);
    
    getResultLD();
    getResultSFD();
    getResultFD();

    getResultOverall();
    generateDownloadLink();

    $('#resultSwitch').change(function() {
        // Clear all data first
        $(".result-data").fadeOut(0)
        $(".result-data").empty()

        if(this.checked)
            getResultOverall()
        else
            getResultOverallRaw()
        
        generateDownloadLink();
        $(".result-data").fadeIn()
    });
});

function getResultLD() {
    let landmarkData = $(".landmark-data");
    landmarkData.append(`
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-hashtag'></i> Number of Landmarks Detected</h5>
        <label class='col-6 data-bold'>Front OCR-Landmarks</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['landmarkFrontOCRNum'] + `</label><br/>
        <label class='col-6 data-bold'>Front Pattern-Landmarks</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['landmarkFrontPatternNum'] + `</label><br/>
        <label class='col-6 data-bold'>Rear OCR-Landmarks</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['landmarkRearOCRNum'] + `</label><br/>
        <label class='col-6 data-bold'>Rear Pattern-Landmarks</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['landmarkRearPatternNum'] + `</label><br/>
        <label class='col-6 data-bold'>Total OCR-Landmarks</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['landmarkTotalOCRNum'] + `</label><br/>
        <label class='col-6 data-bold'>Total Pattern-Landmarks</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['landmarkTotalPatternNum'] + `</label><br/>
        <label class='col-6 data-bold'>Total Landmarks Detected</label><label class='data-bold'>:&nbsp;</label><label class='col-3 data-bold'>` + this.jsonData['landmarkTotalNum'] + `</label><br/>
        
        <hr class='hr-bg-color'>
        
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-id-card'></i> Personal Information</h5>
        <label class='col-3 data-bold'>IC Number</label><label class='data-bold'>:&nbsp;</label><label class='col-8'>` + this.jsonData['frontNRIC'] + `</label><br/>
        <label class='col-3'></label><label>&nbsp;</label><label class='col-8'>(` + this.jsonData['rearNRIC'] + `)</label><br/>
        <label class='col-3 data-bold'>Name</label><label class='data-bold'>:&nbsp;</label><label class='col-8'>` + this.jsonData['name'] + `</label><br/>
        <label class='col-3 data-bold'>Gender</label><label class='data-bold'>:&nbsp;</label><label class='col-8'>` + this.jsonData['gender'] + `</label><br/>
        <label class='col-3 data-bold'>Age</label><label class='data-bold'>:&nbsp;</label><label class='col-8'>` + this.jsonData['age'] + `</label><br/>
        <label class='col-3 data-bold'>Citizenship</label><label class='data-bold'>:&nbsp;</label><label class='col-8'>` + this.jsonData['citizen'] + `</label><br/>
        <label class='col-3 data-bold'>Address</label><label class='data-bold'>:&nbsp;</label><label class='col-8'>` + this.jsonData['address'] + `</label><br/>
    `);
}

function getResultSFD() {
    let securityData = $(".security-data");
    securityData.append(`
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-key'></i> Microprint Detection</h5>
        <label class='col-6 data-bold'>Microprint Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['microprintExistence'] + `</label><br/>
        <label class='col-6 data-bold'>Microprint Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['microprintMatched'] + ` (` + this.jsonData['microprintMatchingPercent'] + `%)</label><br/>
    `);
}

function getResultFD() {
    let fraudData = $(".fraud-data");
    
    fraudData.append(`
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-code-compare'></i> Landmarks Matching</h5>
        <label class='col-6 data-bold'>IC Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['icLogoMatched'] + ` (` + this.jsonData['icLogoMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>MyKad Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['mykadLogoMatched'] + ` (` + this.jsonData['mykadLogoMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Malaysia Flag Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['flagMatched'] + ` (` + this.jsonData['flagMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>MSC Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['mscLogoMatched'] + ` (` + this.jsonData['mscLogoMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Security Chip Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['securityChipMatched'] + ` (` + this.jsonData['securityChipMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Hibiscus Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['hibiscusMatched'] + ` (` + this.jsonData['hibiscusMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Coat of Arms Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['coatOfArmsMatched'] + ` (` + this.jsonData['coatOfArmsMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Touch \'n Go Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['tngMatched'] + ` (` + this.jsonData['tngMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>ATM Logo Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['atmMatched'] + ` (` + this.jsonData['atmMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Signature Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['singatureMatched'] + ` (` + this.jsonData['singatureMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Chip Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['chipMatched'] + ` (` + this.jsonData['chipMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Twin Towers Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['towersMatched'] + ` (` + this.jsonData['towersMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>King\'s Crown Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['crownMatched'] + ` (` + this.jsonData['crownMatchingPercent'] + `%)</label><br/>
        <label class='col-6 data-bold'>Malaysia Wording Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['malaysiaWordingMatched'] + ` (` + this.jsonData['malaysiaWordingMatchingPercent'] + `%)</label><br/>
    
        <hr class='hr-bg-color'>
    
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-bullseye'></i> Blurriness Detection</h5>
        <label class='col-6 data-bold'>Front MyKad is Blurry</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isFrontImageBlurred'] + ` (` + this.jsonData['frontImageBlurriness'] + `%)</label><br/>
        <label class='col-6 data-bold'>Rear MyKad is Blurry</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isRearImageBlurred'] + ` (` + this.jsonData['rearImageBlurriness'] + `%)</label><br/>
    
        <hr class='hr-bg-color'>
    
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-gear'></i> Others</h5>
        <label class='col-6 data-bold'>Valid Front IC Number</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isValidFrontNRIC'] + `</label><br/>
        <label class='col-6 data-bold'>Valid Rear IC Number</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isValidRearNRIC'] + `</label><br/>
        <label class='col-6 data-bold'>Human-Face Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['hasFace'] + `</label><br/>
        <label class='col-6 data-bold'>Valid Pair of MyKad</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isMyKadPair'] + `</label><br/>
    `);
}

function getResultOverall() {
    let resultData = $(".result-data");

    // Supplemental Landmark Verification
    let l_status = (this.jsonData['landmarkDetectionPassed']) ? "Pass" : "Fail";
    let l_color = (this.jsonData['landmarkDetectionPassed']) ? "#0f0" : "#f00";
    let l_score_status = (this.jsonData['landmarksScorePassed']) ? "Pass" : "Fail";
    let l_score_color = (this.jsonData['landmarksScorePassed']) ? "#0f0" : "#f00";
    resultData.append(`
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-location-dot'></i> Supplemental Landmark Verification</h5>

        <label class='col-6 data-bold'>IC Logo Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['icLogoExistence'] + `</label><br/>
        <label class='col-6 data-bold'>MyKad Logo Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['mykadLogoExistence'] + `</label><br/>
        <label class='col-6 data-bold'>Malaysia Flag Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['flagExistence'] + `</label><br/>
        <label class='col-6 data-bold'>Security Chip Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['securityChipExistence'] + `</label><br/>
        <label class='col-6 data-bold'>Coat of Arms Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['coatOfArmsExistence'] + `</label><br/>

        <label class='col-6 data-bold'>Verification Status</label><label class='data-bold'>:&nbsp;</label><label class='col-3' style='color:` + l_color + `;'>` + l_status + `</label><br/>
        <div class='border-score'>
            <label class='col-6 data-bold'>Landmark Overall Score</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['allLandmarksMatchingPercent'] + `% (` + this.jsonData['allLandmarksScore'] + `)</label><br/>
            <label class='col-6 data-bold'>Landmark Score Status</label><label class='data-bold'>:&nbsp;</label><label class='col-3' style='color:` + l_score_color + `;'>` + l_score_status + `</label><br/>
        </div>
    `);

    // Supplemental Security Feature Verification
    let sf_status = (this.jsonData['securityFeatureDetectionPassed']) ? "Pass" : "Fail";
    let sf_color = (this.jsonData['securityFeatureDetectionPassed']) ? "#0f0" : "#f00";
    let sf_score_status = (this.jsonData['securityFeaturesScorePassed']) ? "Pass" : "Fail";
    let sf_score_color = (this.jsonData['securityFeaturesScorePassed']) ? "#0f0" : "#f00";
    resultData.append(`
        <hr class='hr-bg-color'>
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-location-dot'></i> Supplemental Security Feature Verification</h5>

        <label class='col-6 data-bold'>Microprint Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['microprintExistence'] + `</label><br/>
        <label class='col-6 data-bold'>Microprint Matching</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['microprintMatched'] + `</label><br/>

        <label class='col-6 data-bold'>Verification Status</label><label class='data-bold'>:&nbsp;</label><label class='col-3' style='color:` + sf_color + `;'>` + sf_status + `</label><br/>
        <div class='border-score'>
            <label class='col-6 data-bold'>Security Feature Overall Score</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['allSecurityFeaturesPercent'] + `% (` + this.jsonData['allSecurityFeaturesScore'] + `)</label><br/>
            <label class='col-6 data-bold'>Security Feature Score Status</label><label class='data-bold'>:&nbsp;</label><label class='col-3' style='color:` + sf_score_color + `;'>` + sf_score_status + `</label><br/>
        </div>
    `);

    // Supplemental Frauds Verification
    let f_status = (this.jsonData['fraudDetectionPassed']) ? "Pass" : "Fail";
    let f_color = (this.jsonData['fraudDetectionPassed']) ? "#0f0" : "#f00";
    let f_score_status = (this.jsonData['fraudsScorePassed']) ? "Pass" : "Fail";
    let f_score_color = (this.jsonData['fraudsScorePassed']) ? "#0f0" : "#f00";
    resultData.append(`
        <hr class='hr-bg-color'>
        <h5 class='text-center modal-result-header'><i class='fa-solid fa-user-secret'></i> Supplemental Fraud Verification</h5>

        <label class='col-6 data-bold'>Human-Face Existence</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['hasFace'] + `</label><br/>
        <label class='col-6 data-bold'>Valid Front IC Number</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isValidFrontNRIC'] + `</label><br/>
        <label class='col-6 data-bold'>Valid Rear IC Number</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isValidRearNRIC'] + `</label><br/>
        <label class='col-6 data-bold'>Valid Pair of MyKad</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isMyKadPair'] + `</label><br/>
        <label class='col-6 data-bold'>Name is Extracted</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + (this.jsonData['name'] != '') + `</label><br/>
        <label class='col-6 data-bold'>Address is Extracted</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + (this.jsonData['address'] != '') + `</label><br/>
        <label class='col-6 data-bold'>Front MyKad is Blurred</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isFrontImageBlurred'] + `</label><br/>
        <label class='col-6 data-bold'>Rear MyKad is Blurred</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['isRearImageBlurred'] + `</label><br/>

        <label class='col-6 data-bold'>Verification Status</label><label class='data-bold'>:&nbsp;</label><label class='col-3' style='color:` + f_color + `;'>` + f_status + `</label><br/>
        <div class='border-score'>
            <label class='col-6 data-bold'>Fraud Overall Score</label><label class='data-bold'>:&nbsp;</label><label class='col-3'>` + this.jsonData['allFraudsPercent'] + `% (` + this.jsonData['allFraudsScore'] + `)</label><br/>
            <label class='col-6 data-bold'>Fraud Score Status</label><label class='data-bold'>:&nbsp;</label><label class='col-3' style='color:` + f_score_color + `;'>` + f_score_status + `</label><br/>
        </div>
    `);

    // Overall
    let of_score_status = (this.jsonData['finalScorePassed']) ? "Pass" : "Fail";
    let of_score_color = (this.jsonData['finalScorePassed']) ? "#0f0" : "#f00";    
    resultData.append(`
        <hr class='hr-bg-color'>
        <h4 class='text-center pt-5'>Verification Status:&nbsp;<label class='h4' style='color:` + of_score_color + `;'>` + of_score_status + ` (` + this.jsonData['finalPercent'] + `%)</label></h5>
    `);
}

// Display the raw JSON data
function getResultOverallRaw() {
    let resultData = $(".result-data");

    resultData.append(`<pre style='white-space: pre-wrap;'>` + JSON.stringify(this.jsonData, null, 4) + `</pre>`);
}

// To generate the download link
function generateDownloadLink() {
    $(`
        <div class='pb-5 text-center'>
            <i class='fa-solid fa-file-lines'></i>
            &nbsp;
            <a href='javascript:downloadResult()'>Save Result</a>
        </div>
    `).appendTo('.result-data');
}

// To download the generated result file
function downloadResult() {
    let file = 'mykad-verification-result.json';
    let data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(jsonData, null, 4));

    $("<a id='download-result' href='data:" + data + "' download='" + file + "'></a>").appendTo('.result-data');
    document.getElementById('download-result').click();
    $("#download-result").remove();
}