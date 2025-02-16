namespace PriceMap.Model.Sanga;

public class SangaResponse
{
    /// <summary>
    /// 매물번호
    /// </summary>
    public string? atclNo { get; set; }

    /// <summary>
    /// 물건등록일자
    /// </summary>
    public string? atclCfmYmd { get; set; }

    /// <summary>
    /// 물건 구분
    /// </summary>
    public string? rletTpNm { get; set; }

    /// <summary>
    /// 월세 수익률
    /// </summary>
    public double? rateOfReturn { get; set; }

    public double? price { get; set; }

    public double? previousDeposit { get; set; }

    public double? previousMonthlyRent { get; set; }

    public string? curBisType { get; set; }

    /// <summary>
    /// 현재층
    /// </summary>
    public int? curFlow { get; set; }

    /// <summary>
    /// 계약평형
    /// </summary>
    public double? spc1P { get; set; }
    /// <summary>
    /// 전용평형
    /// </summary>
    public double? spc2P { get; set; }

    public double? equilibriumPrice { get; set; }

    public string? atclFetrDesc { get; set; }

    /// <summary>
    /// 계약면적
    /// </summary>
    public double? spc1 { get; set; }

    /// <summary>
    /// 전용면적
    /// </summary>
    public double? spc2 { get; set; }

    /// <summary>
    /// 링크
    /// </summary>
    public string? detaild_information { get; set; }

    public string? regionName { get; set; }

    public string? direction { get; set; }

    public string? buildingUse { get; set; }

    /// <summary>
    /// 주차 가능여부 체크 (Y/N)
    /// </summary>
    public string? parking { get; set; }

    /// <summary>
    /// 전체층
    /// </summary>
    public int? totalFloor { get; set; }

    /// <summary>
    /// 중개사이름
    /// </summary>
    public string? rltrNm { get; set; }

    /// <summary>
    /// 중개사번호
    /// </summary>
    public string? rltrPh { get; set; }
}
