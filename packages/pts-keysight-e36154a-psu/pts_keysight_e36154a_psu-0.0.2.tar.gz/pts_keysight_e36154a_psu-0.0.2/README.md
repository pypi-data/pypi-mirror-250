# Keysight-E36154A-PSU

```
cd keysight-e36154a-psu
git clone git@gitlab.com:pass-testing-solutions/keysight-e36154a-psu.git
git remote add origin https://gitlab.com/pass-testing-solutions/keysight-e36154a-psu.git
git pull origin main
git checkout -b <your-new-branch>  # Please follow the branch naming convention as mentioned in the coding guidelines
```

## Description
This is an interface library for the Keysight E36154A PSU with an Autorange of 30V, 80A, 800W.

## Installation

`pip install keysight_e36154a_psu`

## Usage

### Driver Functions

<span class="target" id="module-pts_keysight_e36154a_psu.keysight_E36154A_psu"><span id="pts-keysight-e36154a-psu"></span></span><dl class="py class">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">pts_keysight_e36154a_psu.keysight_E36154A_psu.</span></span><span class="sig-name descname"><span class="pre">KeySightPsuE36154A</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection_string</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A" title="Permalink to this definition"></a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p><code class="docutils literal notranslate"><span class="pre">Base</span> <span class="pre">class</span> <span class="pre">for</span> <span class="pre">the</span> <span class="pre">Keysight</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.open_connection">
<span class="sig-name descname"><span class="pre">open_connection</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.open_connection" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Opens</span> <span class="pre">a</span> <span class="pre">TCP/IP</span> <span class="pre">connection</span> <span class="pre">to</span> <span class="pre">the</span> <span class="pre">Keysight</span> <span class="pre">DAQ</span> <span class="pre">34980A</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.close_connection">
<span class="sig-name descname"><span class="pre">close_connection</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.close_connection" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Closes</span> <span class="pre">the</span> <span class="pre">TCP/IP</span> <span class="pre">connection</span> <span class="pre">to</span> <span class="pre">the</span> <span class="pre">Keysight</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.factory_reset">
<span class="sig-name descname"><span class="pre">factory_reset</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.factory_reset" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">This</span> <span class="pre">function</span> <span class="pre">helps</span> <span class="pre">factory</span> <span class="pre">reset</span> <span class="pre">the</span> <span class="pre">Keysight</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.selftest">
<span class="sig-name descname"><span class="pre">selftest</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.selftest" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">This</span> <span class="pre">function</span> <span class="pre">self</span> <span class="pre">tests</span> <span class="pre">the</span> <span class="pre">Keysight</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.id_number">
<span class="sig-name descname"><span class="pre">id_number</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.id_number" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">This</span> <span class="pre">function</span> <span class="pre">returns</span> <span class="pre">the</span> <span class="pre">ID</span> <span class="pre">number</span> <span class="pre">of</span> <span class="pre">the</span> <span class="pre">Keysight</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.set_voltage">
<span class="sig-name descname"><span class="pre">set_voltage</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">voltage</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.set_voltage" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Sets</span> <span class="pre">voltage</span> <span class="pre">output</span> <span class="pre">for</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>voltage</strong> – <cite>float</cite> : in Volts</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.set_current">
<span class="sig-name descname"><span class="pre">set_current</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">current</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.set_current" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Sets</span> <span class="pre">current</span> <span class="pre">output</span> <span class="pre">for</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>current</strong> – <cite>float</cite>: in Amps</p>
</dd>
<dt class="field-even">Returns</dt>
<dd class="field-even"><p>None</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_voltage">
<span class="sig-name descname"><span class="pre">check_voltage</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_voltage" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Checks</span> <span class="pre">the</span> <span class="pre">set</span> <span class="pre">voltage</span> <span class="pre">for</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p><cite>float</cite> : voltage in Volts</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_current">
<span class="sig-name descname"><span class="pre">check_current</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_current" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Checks</span> <span class="pre">the</span> <span class="pre">set</span> <span class="pre">current</span> <span class="pre">for</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p><cite>float</cite> : current in Amps</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.measure_voltage">
<span class="sig-name descname"><span class="pre">measure_voltage</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.measure_voltage" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Measures</span> <span class="pre">output</span> <span class="pre">voltage</span> <span class="pre">for</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p><cite>float</cite> : voltage in Volts</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.measure_current">
<span class="sig-name descname"><span class="pre">measure_current</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.measure_current" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Measures</span> <span class="pre">output</span> <span class="pre">current</span> <span class="pre">for</span> <span class="pre">E36154A</span> <span class="pre">PSU</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p><cite>float</cite> : current in Amps</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_min_max_voltage">
<span class="sig-name descname"><span class="pre">check_min_max_voltage</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_min_max_voltage" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Check</span> <span class="pre">the</span> <span class="pre">minimum</span> <span class="pre">and</span> <span class="pre">maximum</span> <span class="pre">voltage</span> <span class="pre">range</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p><cite>Tuple</cite>: Voltage in Volts</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_min_max_current">
<span class="sig-name descname"><span class="pre">check_min_max_current</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_keysight_e36154a_psu.keysight_E36154A_psu.KeySightPsuE36154A.check_min_max_current" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Check</span> <span class="pre">the</span> <span class="pre">minimum</span> <span class="pre">and</span> <span class="pre">maximum</span> <span class="pre">current</span> <span class="pre">range</span></code></p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p><cite>Tuple</cite>: Current in Amps</p>
</dd>
</dl>
</dd></dl>

------------------------------------------------------------------------------------------------------------------------------

## Authors and acknowledgment
Author: Shuparna Deb (@shuparnadeb_pts)

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
